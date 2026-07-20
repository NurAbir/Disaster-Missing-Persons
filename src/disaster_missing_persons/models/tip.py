"""Tip data models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from disaster_missing_persons.models.report import Location


class TipCreate(BaseModel):
    """Tip creation model."""

    report_id: str
    message: str = Field(..., min_length=10, max_length=2000)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    location: Optional[Location] = None
    seen_datetime: Optional[datetime] = None


class TipInDB(TipCreate):
    """Tip model as stored in database."""

    id: str = Field(..., alias="_id")
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    is_read: bool = False
    created_at: datetime

    model_config = {"populate_by_name": True}


class TipResponse(BaseModel):
    """Tip response model for API."""

    id: str
    report_id: str
    message: str
    contact_phone: Optional[str]
    contact_email: Optional[str]
    location: Optional[Location]
    seen_datetime: Optional[datetime]
    user_name: Optional[str]
    is_read: bool
    created_at: datetime
