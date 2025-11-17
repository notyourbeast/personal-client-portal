from datetime import datetime
from typing import Any

from bson import ObjectId


class User:
    collection_name = "users"

    def __init__(self, data: dict[str, Any]):
        self.id: str = str(data.get("_id")) if data.get("_id") else data.get("id")
        self.email: str = data["email"]
        self.full_name: str | None = data.get("full_name")
        self.password_hash: str = data["password_hash"]
        self.created_at: datetime = data.get("created_at", datetime.utcnow())
        self.updated_at: datetime = data.get("updated_at", datetime.utcnow())

    @staticmethod
    def to_document(
        *,
        email: str,
        password_hash: str,
        full_name: str | None = None,
    ) -> dict[str, Any]:
        now = datetime.utcnow()
        return {
            "email": email,
            "full_name": full_name,
            "password_hash": password_hash,
            "created_at": now,
            "updated_at": now,
        }

    @staticmethod
    def object_id(user_id: str) -> ObjectId:
        return ObjectId(user_id)
