from contextlib import asynccontextmanager
from typing import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import get_settings

_settings = get_settings()
_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        try:
            _client = AsyncIOMotorClient(_settings.mongo_uri, serverSelectionTimeoutMS=5000)
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to MongoDB at {_settings.mongo_uri}. "
                f"Please check your MONGO_URI in .env file. Error: {e}"
            ) from e
    return _client


def get_database() -> AsyncIOMotorDatabase:
    return get_client()[_settings.mongo_db]


@asynccontextmanager
async def lifespan(app):  # type: ignore[reportGeneralTypeIssues]
    client = get_client()
    yield
    client.close()
