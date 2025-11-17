from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=100)
    notes: str | None = None


class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=100)
    notes: str | None = None


class ClientResponse(BaseModel):
    id: str
    name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    notes: str | None = None
    created_at: str
    updated_at: str

