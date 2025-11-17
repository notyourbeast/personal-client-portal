from datetime import datetime
from typing import Any

from bson import ObjectId


class Client:
    collection_name = "clients"

    def __init__(self, data: dict[str, Any]):
        self.id: str = str(data.get("_id")) if data.get("_id") else data.get("id")
        self.user_id: str = data["user_id"]
        self.name: str = data["name"]
        self.email: str | None = data.get("email")
        self.phone: str | None = data.get("phone")
        self.company: str | None = data.get("company")
        self.notes: str | None = data.get("notes")
        self.created_at: datetime = data.get("created_at", datetime.utcnow())
        self.updated_at: datetime = data.get("updated_at", datetime.utcnow())

    @staticmethod
    def to_document(
        *,
        user_id: str,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        now = datetime.utcnow()
        return {
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "notes": notes,
            "created_at": now,
            "updated_at": now,
        }

    @staticmethod
    def object_id(client_id: str) -> ObjectId:
        return ObjectId(client_id)

