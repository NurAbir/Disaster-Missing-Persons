"""API routes package."""

from disaster_missing_persons.api.routes.auth import router as auth_router
from disaster_missing_persons.api.routes.admin import router as admin_router
from disaster_missing_persons.api.routes.reports import router as reports_router

__all__ = ["auth_router", "admin_router", "reports_router"]
