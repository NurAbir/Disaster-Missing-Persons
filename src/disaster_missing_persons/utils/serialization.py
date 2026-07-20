"""Data serialization utilities."""

from typing import Any, Dict


def serialize_report(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize a report document from database.

    Args:
        doc: Raw MongoDB document.

    Returns:
        Serialized report dictionary.
    """
    return {
        "id": doc["_id"],
        "full_name": doc["full_name"],
        "age": doc.get("age"),
        "gender": doc.get("gender", "unknown"),
        "height_cm": doc.get("height_cm"),
        "weight_kg": doc.get("weight_kg"),
        "distinguishing_features": doc.get("distinguishing_features"),
        "last_seen_location": doc["last_seen_location"],
        "last_seen_datetime": doc["last_seen_datetime"],
        "clothing_description": doc.get("clothing_description"),
        "medical_conditions": doc.get("medical_conditions"),
        "contact_phone": doc["contact_phone"],
        "contact_email": doc.get("contact_email"),
        "is_urgent": doc.get("is_urgent", False),
        "rescuer_id": doc["rescuer_id"],
        "rescuer_name": doc["rescuer_name"],
        "status": doc["status"],
        "photos": doc.get("photos", []),
        "created_at": doc["created_at"],
        "updated_at": doc.get("updated_at", doc["created_at"]),
        "tips_count": doc.get("tips_count", 0),
    }
