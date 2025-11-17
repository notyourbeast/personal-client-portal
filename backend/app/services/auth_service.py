from fastapi import HTTPException, status
from fastapi.responses import Response

from app.core.security import create_access_token, hash_password, verify_password
from app.core.settings import get_settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schema.auth import LoginRequest, RegisterRequest, UserResponse

settings = get_settings()


class AuthService:
    def __init__(self, repository: UserRepository | None = None) -> None:
        self.repository = repository or UserRepository()

    async def register(self, payload: RegisterRequest) -> User:
        existing = await self.repository.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        document = User.to_document(
            email=payload.email,
            password_hash=hash_password(payload.password),
            full_name=payload.full_name,
        )
        return await self.repository.insert(document)

    async def authenticate(self, payload: LoginRequest) -> User:
        user = await self.repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

    async def login_response(self, response: Response, user: User) -> tuple[UserResponse, str]:
        token = create_access_token(user.id)
        max_age = settings.access_token_expire_minutes * 60
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=settings.environment == "production",
            max_age=max_age,
        )
        user_payload = UserResponse(id=user.id, email=user.email, full_name=user.full_name)
        return user_payload, token

    @staticmethod
    def logout_response(response: Response) -> None:
        response.delete_cookie("access_token")
