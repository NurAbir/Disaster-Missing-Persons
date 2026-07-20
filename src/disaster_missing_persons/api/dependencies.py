"""API dependencies."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from disaster_missing_persons.core.constants import UserRole
from disaster_missing_persons.models.user import UserInDB
from disaster_missing_persons.services.auth_service import decode_token
from disaster_missing_persons.services.database import users_collection

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserInDB:
    """Get the current authenticated user from JWT token.

    Args:
        credentials: HTTP authorization credentials.

    Returns:
        Authenticated user.

    Raises:
        HTTPException: If authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await users_collection.find_one({"_id": user_id})
    if user is None:
        raise credentials_exception

    return UserInDB(**user)


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    """Get current active user.

    Args:
        current_user: Current authenticated user.

    Returns:
        Active user.

    Raises:
        HTTPException: If user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required_role: UserRole):
    """Create a dependency that requires a specific role.

    Args:
        required_role: Required user role.

    Returns:
        Dependency function.
    """

    async def role_checker(
        current_user: UserInDB = Depends(get_current_active_user),
    ) -> UserInDB:
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires {required_role.value} privileges",
            )
        return current_user

    return role_checker


# Convenience dependencies
require_admin = require_role(UserRole.ADMIN)
require_rescuer = require_role(UserRole.RESCUER)
require_user = require_role(UserRole.USER)
