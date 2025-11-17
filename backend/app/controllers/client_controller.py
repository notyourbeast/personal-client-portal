from fastapi import Depends, Query

from app.core.dependencies import get_current_user
from app.schema.auth import UserResponse
from app.schema.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService


async def create_client(
    payload: ClientCreate,
    current_user: UserResponse = Depends(get_current_user),
    service: ClientService = Depends(),
) -> ClientResponse:
    client = await service.create(current_user.id, payload)
    return ClientResponse(
        id=client.id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company=client.company,
        notes=client.notes,
        created_at=client.created_at.isoformat(),
        updated_at=client.updated_at.isoformat(),
    )


async def list_clients(
    search: str | None = Query(default=None, description="Search by name, email, or company"),
    current_user: UserResponse = Depends(get_current_user),
    service: ClientService = Depends(),
) -> list[ClientResponse]:
    clients = await service.list(current_user.id, search)
    return [
        ClientResponse(
            id=c.id,
            name=c.name,
            email=c.email,
            phone=c.phone,
            company=c.company,
            notes=c.notes,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
        )
        for c in clients
    ]


async def get_client(
    client_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: ClientService = Depends(),
) -> ClientResponse:
    client = await service.get(client_id, current_user.id)
    return ClientResponse(
        id=client.id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company=client.company,
        notes=client.notes,
        created_at=client.created_at.isoformat(),
        updated_at=client.updated_at.isoformat(),
    )


async def update_client(
    client_id: str,
    payload: ClientUpdate,
    current_user: UserResponse = Depends(get_current_user),
    service: ClientService = Depends(),
) -> ClientResponse:
    client = await service.update(client_id, current_user.id, payload)
    return ClientResponse(
        id=client.id,
        name=client.name,
        email=client.email,
        phone=client.phone,
        company=client.company,
        notes=client.notes,
        created_at=client.created_at.isoformat(),
        updated_at=client.updated_at.isoformat(),
    )


async def delete_client(
    client_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: ClientService = Depends(),
) -> dict[str, str]:
    await service.delete(client_id, current_user.id)
    return {"detail": "Client deleted"}

