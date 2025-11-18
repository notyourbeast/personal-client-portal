from pydantic import BaseModel, EmailStr, Field, field_validator


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str | None) -> str | None:
        if not v or (isinstance(v, str) and v.strip() == ""):
            return None
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str | None) -> EmailStr | None:
        if v is None:
            return None
        return EmailStr(v)


class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str | None) -> str | None:
        if not v or (isinstance(v, str) and v.strip() == ""):
            return None
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str | None) -> EmailStr | None:
        if v is None:
            return None
        return EmailStr(v)


class ClientResponse(BaseModel):
    id: str
    name: str
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    notes: str | None = None
    created_at: str
    updated_at: str

