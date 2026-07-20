"""User data models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

try:
    from pydantic import EmailStr as _EmailStr
except ImportError:
    _EmailStr = str

from disaster_missing_persons.core.constants import UserRole


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: str
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation model."""

    email: _EmailStr
    password: str = Field(..., min_length=6)


class UserInDB(UserBase):
    """User model as stored in database."""

    id: str = Field(..., alias="_id")
    role: UserRole
    is_active: bool
    created_at: datetime
    organization: Optional[str] = None

    model_config = {"populate_by_name": True}


class UserResponse(UserBase):
    """User response model for API."""

    id: str
    role: UserRole
    is_active: bool
    created_at: datetime
    organization: Optional[str] = None


class RescuerCreate(BaseModel):
    """Rescuer account creation model (admin only)."""

    email: _EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    password: str = Field(..., min_length=6)
    organization: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request model."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str
    user_role: UserRole
    user_name: str
