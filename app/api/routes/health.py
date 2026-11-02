from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return service liveness information."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }
