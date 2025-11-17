from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongo import get_database
from app.models.client import Client


class ClientRepository:
    def __init__(self) -> None:
        db = get_database()
        self.collection: AsyncIOMotorCollection = db[Client.collection_name]

    async def insert(self, document: dict[str, Any]) -> Client:
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return Client(document)

    async def get_by_id(self, client_id: str, user_id: str) -> Client | None:
        from bson import ObjectId

        doc = await self.collection.find_one({"_id": ObjectId(client_id), "user_id": user_id})
        return Client(doc) if doc else None

    async def list_by_user(self, user_id: str, search: str | None = None) -> list[Client]:
        query: dict[str, Any] = {"user_id": user_id}
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"company": {"$regex": search, "$options": "i"}},
            ]
        cursor = self.collection.find(query).sort("created_at", -1)
        docs = await cursor.to_list(length=None)
        return [Client(doc) for doc in docs]

    async def update(self, client_id: str, user_id: str, update_data: dict[str, Any]) -> Client | None:
        from bson import ObjectId

        update_data["updated_at"] = Client.to_document(user_id="", name="")["updated_at"]
        result = await self.collection.update_one(
            {"_id": ObjectId(client_id), "user_id": user_id},
            {"$set": update_data},
        )
        if result.modified_count == 0:
            return None
        return await self.get_by_id(client_id, user_id)

    async def delete(self, client_id: str, user_id: str) -> bool:
        from bson import ObjectId

        result = await self.collection.delete_one({"_id": ObjectId(client_id), "user_id": user_id})
        return result.deleted_count > 0

