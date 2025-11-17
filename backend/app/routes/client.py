from fastapi import APIRouter

from app.controllers import client_controller
from app.schema.client import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientResponse, status_code=201)
async def create(payload: ClientCreate) -> ClientResponse:
    return await client_controller.create_client(payload)


@router.get("", response_model=list[ClientResponse])
async def list_clients() -> list[ClientResponse]:
    return await client_controller.list_clients()


@router.get("/{client_id}", response_model=ClientResponse)
async def get(client_id: str) -> ClientResponse:
    return await client_controller.get_client(client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update(client_id: str, payload: ClientUpdate) -> ClientResponse:
    return await client_controller.update_client(client_id, payload)


@router.delete("/{client_id}", status_code=204)
async def delete(client_id: str) -> None:
    from fastapi import Response

    await client_controller.delete_client(client_id)
    return Response(status_code=204)

