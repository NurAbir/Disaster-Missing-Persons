"""Database service layer."""

from motor.motor_asyncio import AsyncIOMotorClient
from disaster_missing_persons.core.config import get_settings
from disaster_missing_persons.core.constants import (
    COLLECTION_USERS,
    COLLECTION_REPORTS,
    COLLECTION_TIPS,
)
import bcrypt

settings = get_settings()

# MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# Collection references
users_collection = db[COLLECTION_USERS]
reports_collection = db[COLLECTION_REPORTS]
tips_collection = db[COLLECTION_TIPS]


async def init_database() -> None:
    """Initialize database with indexes and default data."""
    # Users indexes
    await users_collection.create_index("email", unique=True)
    await users_collection.create_index("username", unique=True)

    # Reports indexes
    await reports_collection.create_index("status")
    await reports_collection.create_index("created_at")
    await reports_collection.create_index("rescuer_id")
    await reports_collection.create_index([("last_seen_location", "2dsphere")])

    # Tips indexes
    await tips_collection.create_index("report_id")
    await tips_collection.create_index("created_at")

    # Fix any existing admin with invalid email
    from datetime import datetime
    from bson import ObjectId

    # Check if there's an admin with the old invalid email
    old_admin = await users_collection.find_one({"email": "admin@disaster.local"})
    if old_admin:
        # Delete the old invalid admin so we can recreate with valid email
        await users_collection.delete_one({"_id": old_admin["_id"]})
        print("Removed old admin with invalid email")

    # Create default admin if none exists
    admin_exists = await users_collection.find_one({"role": "admin"})

    if not admin_exists:
        hashed = bcrypt.hashpw(
            settings.DEFAULT_ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        await users_collection.insert_one(
            {
                "_id": str(ObjectId()),
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "username": "admin",
                "full_name": "System Administrator",
                "hashed_password": hashed,
                "role": "admin",
                "is_active": True,
                "created_at": datetime.utcnow(),
            }
        )
        print(f"Default admin created: {settings.DEFAULT_ADMIN_EMAIL}")
