"""Missing person report routes."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId

from disaster_missing_persons.core.constants import REPORTS_PREFIX, ReportStatus, UserRole
from disaster_missing_persons.models.user import UserInDB
from disaster_missing_persons.models.report import (
    ReportCreate,
    ReportResponse,
    ReportListItem,
    ReportStatusUpdate,
)
from disaster_missing_persons.models.tip import TipCreate, TipResponse
from disaster_missing_persons.services.database import reports_collection, tips_collection
from disaster_missing_persons.api.dependencies import get_current_active_user, require_rescuer
from disaster_missing_persons.utils.image import compress_image
from disaster_missing_persons.utils.datetime import calculate_expiry_date
from disaster_missing_persons.utils.serialization import serialize_report

router = APIRouter(prefix=REPORTS_PREFIX, tags=["reports"])


@router.get("/stats")
async def get_public_stats() -> dict:
    """Get public system statistics (no auth required)."""
    from disaster_missing_persons.services.database import reports_collection, tips_collection

    active_reports = await reports_collection.count_documents({"status": "active"})
    found_persons = await reports_collection.count_documents({"status": "found"})
    total_tips = await tips_collection.count_documents({})
    urgent_reports = await reports_collection.count_documents(
        {"is_urgent": True, "status": "active"}
    )
    return {
        "active_reports": active_reports,
        "found_persons": found_persons,
        "total_tips": total_tips,
        "urgent_reports": urgent_reports,
    }


@router.get("/", response_model=List[ReportListItem])
async def list_reports(
    status: Optional[ReportStatus] = Query(None),
    urgent_only: bool = Query(False),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> List[ReportListItem]:
    """List missing person reports (public access).

    Anyone can view active missing person reports. Supports filtering
    by status, urgency, and text search.

    Args:
        status: Filter by report status.
        urgent_only: Show only urgent reports.
        search: Search by name, features, or clothing.
        skip: Pagination offset.
        limit: Pagination limit.

    Returns:
        List of report list items.
    """
    query = {}

    if status:
        query["status"] = status.value
    else:
        query["status"] = {"$in": ["active", "found"]}

    if urgent_only:
        query["is_urgent"] = True

    if search:
        query["$or"] = [
            {"full_name": {"$regex": search, "$options": "i"}},
            {"distinguishing_features": {"$regex": search, "$options": "i"}},
            {"clothing_description": {"$regex": search, "$options": "i"}},
        ]

    reports = []
    cursor = reports_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)

    async for doc in cursor:
        reports.append(
            ReportListItem(
                id=doc["_id"],
                full_name=doc["full_name"],
                age=doc.get("age"),
                gender=doc.get("gender", "unknown"),
                last_seen_location=doc["last_seen_location"],
                last_seen_datetime=doc["last_seen_datetime"],
                is_urgent=doc.get("is_urgent", False),
                status=doc["status"],
                created_at=doc["created_at"],
                photos=doc.get("photos", [])[:1],
                tips_count=doc.get("tips_count", 0),
            )
        )

    return reports


@router.post("/", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    current_user: UserInDB = Depends(require_rescuer),
) -> ReportResponse:
    """Create a missing person report (rescuers only).

    Only authorized rescuers can create missing person reports.
    Photos are automatically compressed for bandwidth efficiency.

    Args:
        report_data: Report creation data.
        current_user: Authenticated rescuer (injected).

    Returns:
        Created report.
    """
    compressed_photos = []
    for photo in report_data.photos or []:
        if photo:
            compressed = compress_image(photo)
            compressed_photos.append(compressed)

    now = datetime.utcnow()
    report_doc = {
        "_id": str(ObjectId()),
        "full_name": report_data.full_name,
        "age": report_data.age,
        "gender": report_data.gender.value,
        "height_cm": report_data.height_cm,
        "weight_kg": report_data.weight_kg,
        "distinguishing_features": report_data.distinguishing_features,
        "last_seen_location": report_data.last_seen_location.model_dump(),
        "last_seen_datetime": report_data.last_seen_datetime,
        "clothing_description": report_data.clothing_description,
        "medical_conditions": report_data.medical_conditions,
        "contact_phone": report_data.contact_phone,
        "contact_email": report_data.contact_email,
        "is_urgent": report_data.is_urgent,
        "rescuer_id": current_user.id,
        "rescuer_name": current_user.full_name,
        "status": ReportStatus.ACTIVE.value,
        "photos": compressed_photos,
        "created_at": now,
        "updated_at": now,
        "expires_at": calculate_expiry_date(),
        "tips_count": 0,
    }

    await reports_collection.insert_one(report_doc)

    return ReportResponse(**serialize_report(report_doc))


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str) -> ReportResponse:
    """Get a specific report (public access).

    Args:
        report_id: Report ID.

    Returns:
        Report details.

    Raises:
        HTTPException: If report not found.
    """
    doc = await reports_collection.find_one({"_id": report_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportResponse(**serialize_report(doc))


@router.patch("/{report_id}/status")
async def update_report_status(
    report_id: str,
    status_update: ReportStatusUpdate,
    current_user: UserInDB = Depends(require_rescuer),
) -> dict:
    """Update report status (rescuer who created it or admin).

    Args:
        report_id: Report ID.
        status_update: New status.
        current_user: Authenticated rescuer (injected).

    Returns:
        Success message.

    Raises:
        HTTPException: If not authorized or report not found.
    """
    report = await reports_collection.find_one({"_id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Any rescuer or admin can change any report status
    if current_user.role not in (UserRole.RESCUER, UserRole.ADMIN):
        raise HTTPException(
            status_code=403, detail="Only rescuers and admins can change report status"
        )

    await reports_collection.update_one(
        {"_id": report_id},
        {"$set": {"status": status_update.status.value, "updated_at": datetime.utcnow()}},
    )

    return {"message": f"Report status updated to {status_update.status.value}"}


@router.post("/{report_id}/tips")
async def submit_tip(
    report_id: str,
    tip_data: TipCreate,
    current_user: UserInDB = Depends(get_current_active_user),
) -> dict:
    """Submit a tip about a missing person (any authenticated user).

    Users can submit tips with information about a missing person's
    whereabouts. Tips are only accepted for active reports.

    Args:
        report_id: Report ID.
        tip_data: Tip data.
        current_user: Authenticated user (injected).

    Returns:
        Success message with tip ID.

    Raises:
        HTTPException: If report not found or not active.
    """
    report = await reports_collection.find_one(
        {
            "_id": report_id,
            "status": ReportStatus.ACTIVE.value,
        }
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or not active")

    tip_doc = {
        "_id": str(ObjectId()),
        "report_id": report_id,
        "message": tip_data.message,
        "contact_phone": tip_data.contact_phone,
        "contact_email": tip_data.contact_email,
        "location": tip_data.location.model_dump() if tip_data.location else None,
        "seen_datetime": tip_data.seen_datetime,
        "user_id": current_user.id,
        "user_name": current_user.full_name,
        "is_read": False,
        "created_at": datetime.utcnow(),
    }

    await tips_collection.insert_one(tip_doc)

    await reports_collection.update_one(
        {"_id": report_id},
        {"$inc": {"tips_count": 1}},
    )

    return {"message": "Tip submitted successfully", "tip_id": tip_doc["_id"]}


@router.get("/{report_id}/tips")
async def get_report_tips(
    report_id: str,
    current_user: UserInDB = Depends(require_rescuer),
) -> List[TipResponse]:
    """Get tips for a report (rescuer who owns it or admin).

    Automatically marks all tips as read when viewed.

    Args:
        report_id: Report ID.
        current_user: Authenticated rescuer (injected).

    Returns:
        List of tips.

    Raises:
        HTTPException: If not authorized or report not found.
    """
    report = await reports_collection.find_one({"_id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report["rescuer_id"] != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view these tips")

    tips = []
    async for doc in tips_collection.find({"report_id": report_id}).sort("created_at", -1):
        tips.append(
            TipResponse(
                id=doc["_id"],
                report_id=doc["report_id"],
                message=doc["message"],
                contact_phone=doc.get("contact_phone"),
                contact_email=doc.get("contact_email"),
                location=doc.get("location"),
                seen_datetime=doc.get("seen_datetime"),
                user_name=doc.get("user_name"),
                is_read=doc.get("is_read", False),
                created_at=doc["created_at"],
            )
        )

    await tips_collection.update_many(
        {"report_id": report_id, "is_read": False},
        {"$set": {"is_read": True}},
    )

    return tips
