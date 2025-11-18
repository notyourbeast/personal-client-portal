from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    client_id: str
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: str = Field(default="idea", pattern="^(idea|talks|in-progress|review|completed)$")
    hourly_rate: float | None = Field(default=None, ge=0)
    deadline: datetime | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: str | None = Field(default=None, pattern="^(idea|talks|in-progress|review|completed)$")
    hourly_rate: float | None = Field(default=None, ge=0)
    deadline: datetime | None = None


class ProjectStatusUpdate(BaseModel):
    status: str = Field(pattern="^(idea|talks|in-progress|review|completed)$")


class ProjectResponse(BaseModel):
    id: str
    client_id: str
    title: str
    description: str | None = None
    status: str
    hourly_rate: float | None = None
    deadline: str | None = None
    created_at: str
    updated_at: str

