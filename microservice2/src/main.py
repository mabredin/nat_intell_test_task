from fastapi import FastAPI

from api import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Test API")

    app.include_router(api_router)

    return app
