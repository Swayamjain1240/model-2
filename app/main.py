from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import RequestIdMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.add_middleware(RequestIdMiddleware)
    application.include_router(health_router, prefix="/api")
    application.include_router(auth_router, prefix="/api")
    return application


app = create_app()
