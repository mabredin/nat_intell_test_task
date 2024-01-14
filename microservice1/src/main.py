from typing import Any

from fastapi import FastAPI

from api.router import api_router
from config import app_settings


def create_app() -> FastAPI:
    app_configuration: dict[str, Any] = {"title": app_settings.PROJECT_NAME}

    if not app_settings.DEBUG:
        app_configuration.update({"docs_url": None, "redoc_url": None})

    app = FastAPI(**app_configuration)

    app.include_router(api_router, prefix="/api")

    return app
