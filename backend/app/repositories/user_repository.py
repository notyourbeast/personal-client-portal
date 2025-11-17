from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongo import get_database
from app.models.user import User


class UserRepository:
    def __init__(self) -> None:
        db = get_database()
        self.collection: AsyncIOMotorCollection = db[User.collection_name]

    async def insert(self, document: dict[str, Any]) -> User:
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return User(document)

    async def get_by_email(self, email: str) -> User | None:
        doc = await self.collection.find_one({"email": email})
        return User(doc) if doc else None

    async def get_by_id(self, user_id: str) -> User | None:
        from bson import ObjectId

        doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        return User(doc) if doc else None
