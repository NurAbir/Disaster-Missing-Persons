"""Application constants."""

from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    RESCUER = "rescuer"
    USER = "user"


class ReportStatus(str, Enum):
    """Missing person report status enumeration."""

    ACTIVE = "active"
    FOUND = "found"
    CLOSED = "closed"


class Gender(str, Enum):
    """Gender enumeration."""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


# Collection names
COLLECTION_USERS = "users"
COLLECTION_REPORTS = "reports"
COLLECTION_TIPS = "tips"

# API prefixes
API_PREFIX = "/api"
AUTH_PREFIX = f"{API_PREFIX}/auth"
ADMIN_PREFIX = f"{API_PREFIX}/admin"
REPORTS_PREFIX = f"{API_PREFIX}/reports"

# Token settings
TOKEN_TYPE = "bearer"
