from fastapi import APIRouter

from app.controllers import project_controller
from app.schema.project import ProjectCreate, ProjectResponse, ProjectStatusUpdate, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create(payload: ProjectCreate) -> ProjectResponse:
    return await project_controller.create_project(payload)


@router.get("", response_model=list[ProjectResponse])
async def list_projects() -> list[ProjectResponse]:
    return await project_controller.list_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get(project_id: str) -> ProjectResponse:
    return await project_controller.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update(project_id: str, payload: ProjectUpdate) -> ProjectResponse:
    return await project_controller.update_project(project_id, payload)


@router.patch("/{project_id}/status", response_model=ProjectResponse)
async def update_status(project_id: str, payload: ProjectStatusUpdate) -> ProjectResponse:
    return await project_controller.update_project_status(project_id, payload)


@router.delete("/{project_id}", status_code=204)
async def delete(project_id: str) -> None:
    from fastapi import Response

    await project_controller.delete_project(project_id)
    return Response(status_code=204)

