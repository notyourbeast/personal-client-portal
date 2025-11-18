from fastapi import Depends, Query

from app.core.dependencies import get_current_user
from app.schema.auth import UserResponse
from app.schema.project import ProjectCreate, ProjectResponse, ProjectStatusUpdate, ProjectUpdate
from app.services.project_service import ProjectService


async def create_project(
    payload: ProjectCreate,
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> ProjectResponse:
    project = await service.create(current_user.id, payload)
    return ProjectResponse(
        id=project.id,
        client_id=project.client_id,
        title=project.title,
        description=project.description,
        status=project.status,
        hourly_rate=project.hourly_rate,
        deadline=project.deadline.isoformat() if project.deadline else None,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


async def list_projects(
    client_id: str | None = Query(default=None, description="Filter by client ID"),
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> list[ProjectResponse]:
    projects = await service.list(current_user.id, client_id)
    return [
        ProjectResponse(
            id=p.id,
            client_id=p.client_id,
            title=p.title,
            description=p.description,
            status=p.status,
            hourly_rate=p.hourly_rate,
            deadline=p.deadline.isoformat() if p.deadline else None,
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat(),
        )
        for p in projects
    ]


async def get_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> ProjectResponse:
    project = await service.get(project_id, current_user.id)
    return ProjectResponse(
        id=project.id,
        client_id=project.client_id,
        title=project.title,
        description=project.description,
        status=project.status,
        hourly_rate=project.hourly_rate,
        deadline=project.deadline.isoformat() if project.deadline else None,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> ProjectResponse:
    project = await service.update(project_id, current_user.id, payload)
    return ProjectResponse(
        id=project.id,
        client_id=project.client_id,
        title=project.title,
        description=project.description,
        status=project.status,
        hourly_rate=project.hourly_rate,
        deadline=project.deadline.isoformat() if project.deadline else None,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


async def update_project_status(
    project_id: str,
    payload: ProjectStatusUpdate,
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> ProjectResponse:
    project = await service.update_status(project_id, current_user.id, payload)
    return ProjectResponse(
        id=project.id,
        client_id=project.client_id,
        title=project.title,
        description=project.description,
        status=project.status,
        hourly_rate=project.hourly_rate,
        deadline=project.deadline.isoformat() if project.deadline else None,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


async def delete_project(
    project_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: ProjectService = Depends(),
) -> dict[str, str]:
    await service.delete(project_id, current_user.id)
    return {"detail": "Project deleted"}

