"""Admin routes."""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from disaster_missing_persons.core.constants import ADMIN_PREFIX, UserRole
from disaster_missing_persons.models.user import RescuerCreate, UserResponse
from disaster_missing_persons.services.database import (
    users_collection,
    reports_collection,
    tips_collection,
)
from disaster_missing_persons.services.auth_service import get_password_hash
from disaster_missing_persons.api.dependencies import require_admin

router = APIRouter(prefix=ADMIN_PREFIX, tags=["admin"])


@router.post("/create-rescuer", response_model=UserResponse)
async def create_rescuer(
    rescuer_data: RescuerCreate,
    admin=Depends(require_admin),
) -> UserResponse:
    """Create a new rescuer account (admin only).

    Only administrators can create rescuer accounts. Rescuers can create
    missing person reports and view tips on their reports.

    Args:
        rescuer_data: Rescuer account data.
        admin: Current admin user (injected).

    Returns:
        Created rescuer user.

    Raises:
        HTTPException: If email or username already exists.
    """
    existing = await users_collection.find_one(
        {
            "$or": [
                {"email": rescuer_data.email},
                {"username": rescuer_data.username},
            ]
        }
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already exists",
        )

    rescuer_doc = {
        "_id": str(ObjectId()),
        "email": rescuer_data.email,
        "username": rescuer_data.username,
        "full_name": rescuer_data.full_name,
        "phone": rescuer_data.phone,
        "organization": rescuer_data.organization,
        "hashed_password": get_password_hash(rescuer_data.password),
        "role": UserRole.RESCUER.value,
        "is_active": True,
        "created_at": datetime.utcnow(),
    }

    await users_collection.insert_one(rescuer_doc)

    return UserResponse(
        id=rescuer_doc["_id"],
        email=rescuer_doc["email"],
        username=rescuer_doc["username"],
        full_name=rescuer_doc["full_name"],
        phone=rescuer_doc.get("phone"),
        role=UserRole.RESCUER,
        is_active=True,
        created_at=rescuer_doc["created_at"],
        organization=rescuer_doc.get("organization"),
    )


@router.get("/rescuers")
async def list_rescuers(admin=Depends(require_admin)) -> list[dict]:
    """List all rescuer accounts (admin only).

    Args:
        admin: Current admin user (injected).

    Returns:
        List of rescuer accounts.
    """
    rescuers = []
    async for doc in users_collection.find({"role": UserRole.RESCUER.value}):
        rescuers.append(
            {
                "id": doc["_id"],
                "email": doc["email"],
                "username": doc["username"],
                "full_name": doc["full_name"],
                "phone": doc.get("phone"),
                "organization": doc.get("organization"),
                "is_active": doc.get("is_active", True),
                "created_at": doc["created_at"].isoformat() if "created_at" in doc else None,
            }
        )
    return rescuers


@router.get("/stats")
async def get_stats(admin=Depends(require_admin)) -> dict:
    """Get system statistics (admin only).

    Args:
        admin: Current admin user (injected).

    Returns:
        System statistics.
    """
    total_reports = await reports_collection.count_documents({})
    active_reports = await reports_collection.count_documents({"status": "active"})
    found_persons = await reports_collection.count_documents({"status": "found"})
    total_tips = await tips_collection.count_documents({})
    urgent_reports = await reports_collection.count_documents(
        {"is_urgent": True, "status": "active"}
    )

    return {
        "total_reports": total_reports,
        "active_reports": active_reports,
        "found_persons": found_persons,
        "total_tips": total_tips,
        "urgent_reports": urgent_reports,
    }
