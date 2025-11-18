from fastapi import HTTPException, status

from app.models.project import Project
from app.repositories.client_repository import ClientRepository
from app.repositories.project_repository import ProjectRepository
from app.schema.project import ProjectCreate, ProjectStatusUpdate, ProjectUpdate


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository | None = None,
        client_repository: ClientRepository | None = None,
    ) -> None:
        self.repository = repository or ProjectRepository()
        self.client_repository = client_repository or ClientRepository()

    async def create(self, user_id: str, payload: ProjectCreate) -> Project:
        client = await self.client_repository.get_by_id(payload.client_id, user_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        document = Project.to_document(
            user_id=user_id,
            client_id=payload.client_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            hourly_rate=payload.hourly_rate,
            deadline=payload.deadline,
        )
        return await self.repository.insert(document)

    async def list(self, user_id: str, client_id: str | None = None) -> list[Project]:
        return await self.repository.list_by_user(user_id, client_id)

    async def get(self, project_id: str, user_id: str) -> Project:
        project = await self.repository.get_by_id(project_id, user_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def update(self, project_id: str, user_id: str, payload: ProjectUpdate) -> Project:
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(project_id, user_id)

        project = await self.repository.update(project_id, user_id, update_data)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def update_status(self, project_id: str, user_id: str, payload: ProjectStatusUpdate) -> Project:
        project = await self.repository.update_status(project_id, user_id, payload.status)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    async def delete(self, project_id: str, user_id: str) -> None:
        deleted = await self.repository.delete(project_id, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

