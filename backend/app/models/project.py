from datetime import datetime
from typing import Any

from bson import ObjectId


class Project:
    collection_name = "projects"
    STATUS_CHOICES = ["idea", "talks", "in-progress", "review", "completed"]

    def __init__(self, data: dict[str, Any]):
        self.id: str = str(data.get("_id")) if data.get("_id") else data.get("id")
        self.user_id: str = data["user_id"]
        self.client_id: str = data["client_id"]
        self.title: str = data["title"]
        self.description: str | None = data.get("description")
        self.status: str = data.get("status", "idea")
        self.hourly_rate: float | None = data.get("hourly_rate")
        self.deadline: datetime | None = data.get("deadline")
        self.created_at: datetime = data.get("created_at", datetime.utcnow())
        self.updated_at: datetime = data.get("updated_at", datetime.utcnow())

    @staticmethod
    def to_document(
        *,
        user_id: str,
        client_id: str,
        title: str,
        description: str | None = None,
        status: str = "idea",
        hourly_rate: float | None = None,
        deadline: datetime | None = None,
    ) -> dict[str, Any]:
        now = datetime.utcnow()
        return {
            "user_id": user_id,
            "client_id": client_id,
            "title": title,
            "description": description,
            "status": status,
            "hourly_rate": hourly_rate,
            "deadline": deadline,
            "created_at": now,
            "updated_at": now,
        }

    @staticmethod
    def object_id(project_id: str) -> ObjectId:
        return ObjectId(project_id)

