from fastapi import HTTPException, status

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schema.client import ClientCreate, ClientResponse, ClientUpdate


class ClientService:
    def __init__(self, repository: ClientRepository | None = None) -> None:
        self.repository = repository or ClientRepository()

    async def create(self, user_id: str, payload: ClientCreate) -> Client:
        document = Client.to_document(
            user_id=user_id,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
            notes=payload.notes,
        )
        return await self.repository.insert(document)

    async def list(self, user_id: str, search: str | None = None) -> list[Client]:
        return await self.repository.list_by_user(user_id, search)

    async def get(self, client_id: str, user_id: str) -> Client:
        client = await self.repository.get_by_id(client_id, user_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client

    async def update(self, client_id: str, user_id: str, payload: ClientUpdate) -> Client:
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(client_id, user_id)

        client = await self.repository.update(client_id, user_id, update_data)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client

    async def delete(self, client_id: str, user_id: str) -> None:
        deleted = await self.repository.delete(client_id, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

