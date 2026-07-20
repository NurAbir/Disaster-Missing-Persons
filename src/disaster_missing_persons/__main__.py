"""Entry point for running the application."""

import uvicorn
from disaster_missing_persons.core.config import get_settings

settings = get_settings()


def main() -> None:
    """Run the application with uvicorn."""
    uvicorn.run(
        "disaster_missing_persons.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
