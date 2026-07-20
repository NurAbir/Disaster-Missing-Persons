"""Date and time utilities."""

from datetime import datetime, timedelta
from typing import Optional

from disaster_missing_persons.core.config import get_settings

settings = get_settings()


def calculate_expiry_date(days: Optional[int] = None) -> datetime:
    """Calculate report expiry date.

    Args:
        days: Number of days until expiry. Defaults to REPORT_AUTO_EXPIRE_DAYS.

    Returns:
        Expiry datetime.
    """
    days = days or settings.REPORT_AUTO_EXPIRE_DAYS
    return datetime.utcnow() + timedelta(days=days)


def format_datetime(dt: datetime) -> str:
    """Format datetime for display.

    Args:
        dt: Datetime object.

    Returns:
        Formatted string.
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def parse_datetime(dt_str: str) -> datetime:
    """Parse datetime string.

    Args:
        dt_str: Datetime string.

    Returns:
        Parsed datetime object.
    """
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
