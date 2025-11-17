from fastapi import Depends, Response

from app.core.dependencies import get_current_user
from app.schema.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from app.services.auth_service import AuthService


async def register_user(payload: RegisterRequest, service: AuthService = Depends()) -> UserResponse:
    user = await service.register(payload)
    return UserResponse(id=user.id, email=user.email, full_name=user.full_name)


async def login_user(
    payload: LoginRequest,
    response: Response,
    service: AuthService = Depends(),
) -> AuthResponse:
    user = await service.authenticate(payload)
    user_response, token = await service.login_response(response, user)
    return AuthResponse(user=user_response, access_token=token)


async def logout_user(response: Response) -> dict[str, str]:
    AuthService.logout_response(response)
    return {"detail": "Logged out"}


async def current_user(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user
