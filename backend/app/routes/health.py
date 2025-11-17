from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Service availability probe")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
