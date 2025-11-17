from contextlib import asynccontextmanager
from typing import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import get_settings

_settings = get_settings()
_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(_settings.mongo_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    return get_client()[_settings.mongo_db]


@asynccontextmanager
async def lifespan(app):  # type: ignore[reportGeneralTypeIssues]
    client = get_client()
    yield
    client.close()
