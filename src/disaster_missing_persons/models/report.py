"""Missing person report data models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from disaster_missing_persons.core.constants import ReportStatus, Gender


class Location(BaseModel):
    """Geographic location model."""

    latitude: float = Field(default=0.0, ge=-90, le=90)
    longitude: float = Field(default=0.0, ge=-180, le=180)
    address: Optional[str] = None
    description: Optional[str] = None


class ReportBase(BaseModel):
    """Base report model with common fields."""

    full_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Gender = Gender.UNKNOWN
    height_cm: Optional[int] = Field(None, ge=50, le=250)
    weight_kg: Optional[int] = Field(None, ge=10, le=300)
    distinguishing_features: Optional[str] = None
    last_seen_location: Location
    last_seen_datetime: datetime
    clothing_description: Optional[str] = None
    medical_conditions: Optional[str] = None
    contact_phone: str
    contact_email: Optional[str] = None
    is_urgent: bool = False


class ReportCreate(ReportBase):
    """Report creation model."""

    photos: Optional[List[str]] = []


class ReportInDB(ReportBase):
    """Report model as stored in database."""

    id: str = Field(..., alias="_id")
    rescuer_id: str
    rescuer_name: str
    status: ReportStatus
    photos: List[str]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    tips_count: int = 0

    model_config = {"populate_by_name": True}


class ReportResponse(ReportBase):
    """Report response model for API."""

    id: str
    rescuer_id: str
    rescuer_name: str
    status: ReportStatus
    photos: List[str]
    created_at: datetime
    updated_at: datetime
    tips_count: int


class ReportListItem(BaseModel):
    """Report list item for listing endpoints."""

    id: str
    full_name: str
    age: Optional[int]
    gender: Gender
    last_seen_location: Location
    last_seen_datetime: datetime
    is_urgent: bool
    status: ReportStatus
    created_at: datetime
    photos: List[str]
    tips_count: int


class ReportStatusUpdate(BaseModel):
    """Report status update model."""

    status: ReportStatus
