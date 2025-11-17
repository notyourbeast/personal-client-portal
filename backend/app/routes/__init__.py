from fastapi import APIRouter

from app.routes import auth, client, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(client.router)
