from fastapi import APIRouter, Depends, Response

from app.controllers import auth_controller
from app.core.dependencies import get_current_user
from app.schema.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest) -> UserResponse:
    return await auth_controller.register_user(payload)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, response: Response) -> AuthResponse:
    return await auth_controller.login_user(payload, response)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    return await auth_controller.logout_user(response)


@router.get("/me", response_model=UserResponse)
async def me(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user
