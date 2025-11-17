from fastapi import Cookie, Depends, HTTPException, status

from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.schema.auth import UserResponse


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    repository: UserRepository = Depends(),
) -> UserResponse:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(access_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserResponse(id=user.id, email=user.email, full_name=user.full_name)
