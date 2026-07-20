"""Authentication routes."""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from disaster_missing_persons.core.constants import AUTH_PREFIX, UserRole
from disaster_missing_persons.models.user import UserCreate, LoginRequest, TokenResponse
from disaster_missing_persons.services.database import users_collection
from disaster_missing_persons.services.auth_service import (
    verify_password,
    get_password_hash,
    create_access_token,
)

router = APIRouter(prefix=AUTH_PREFIX, tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserCreate) -> TokenResponse:
    """Register a new public user account.

    Anyone can create a user account to submit tips about missing persons.

    Args:
        user_data: User registration data.

    Returns:
        JWT access token.

    Raises:
        HTTPException: If email or username already exists.
    """
    existing = await users_collection.find_one(
        {
            "$or": [
                {"email": user_data.email},
                {"username": user_data.username},
            ]
        }
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )

    user_doc = {
        "_id": str(ObjectId()),
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "phone": user_data.phone,
        "hashed_password": get_password_hash(user_data.password),
        "role": UserRole.USER.value,
        "is_active": True,
        "created_at": datetime.utcnow(),
    }

    await users_collection.insert_one(user_doc)

    token = create_access_token({"sub": user_doc["_id"], "role": user_doc["role"]})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_role=UserRole.USER,
        user_name=user_data.full_name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest) -> TokenResponse:
    """Login for all user types.

    Supports login by username or email.

    Args:
        credentials: Login credentials.

    Returns:
        JWT access token.

    Raises:
        HTTPException: If credentials are invalid.
    """
    user = await users_collection.find_one(
        {
            "$or": [
                {"username": credentials.username},
                {"email": credentials.username},
            ]
        }
    )

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Account is deactivated")

    token = create_access_token({"sub": user["_id"], "role": user["role"]})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_role=UserRole(user["role"]),
        user_name=user["full_name"],
    )
