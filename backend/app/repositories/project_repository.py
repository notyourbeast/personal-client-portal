from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongo import get_database
from app.models.project import Project


class ProjectRepository:
    def __init__(self) -> None:
        db = get_database()
        self.collection: AsyncIOMotorCollection = db[Project.collection_name]

    async def insert(self, document: dict[str, Any]) -> Project:
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return Project(document)

    async def get_by_id(self, project_id: str, user_id: str) -> Project | None:
        from bson import ObjectId

        doc = await self.collection.find_one({"_id": ObjectId(project_id), "user_id": user_id})
        return Project(doc) if doc else None

    async def list_by_user(self, user_id: str, client_id: str | None = None) -> list[Project]:
        query: dict[str, Any] = {"user_id": user_id}
        if client_id:
            query["client_id"] = client_id
        cursor = self.collection.find(query).sort("created_at", -1)
        docs = await cursor.to_list(length=None)
        return [Project(doc) for doc in docs]

    async def update(self, project_id: str, user_id: str, update_data: dict[str, Any]) -> Project | None:
        from bson import ObjectId

        update_data["updated_at"] = Project.to_document(user_id="", client_id="", title="")["updated_at"]
        result = await self.collection.update_one(
            {"_id": ObjectId(project_id), "user_id": user_id},
            {"$set": update_data},
        )
        if result.modified_count == 0:
            return None
        return await self.get_by_id(project_id, user_id)

    async def update_status(self, project_id: str, user_id: str, status: str) -> Project | None:
        from bson import ObjectId

        result = await self.collection.update_one(
            {"_id": ObjectId(project_id), "user_id": user_id},
            {"$set": {"status": status, "updated_at": Project.to_document(user_id="", client_id="", title="")["updated_at"]}},
        )
        if result.modified_count == 0:
            return None
        return await self.get_by_id(project_id, user_id)

    async def delete(self, project_id: str, user_id: str) -> bool:
        from bson import ObjectId

        result = await self.collection.delete_one({"_id": ObjectId(project_id), "user_id": user_id})
        return result.deleted_count > 0

