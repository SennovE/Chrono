from logging import getLogger
from fastapi import FastAPI
from uvicorn import run
from app.config import DefaultSettings, get_settings
from app.endpoints import list_of_routes
logger = getLogger(__name__)


def bindRoutes(application: FastAPI, setting: DefaultSettings) -> None:
     for route in list_of_routes:
       application.include_router(route, prefix=setting.PATH_PREFIX)


def getApp() -> FastAPI:
    application = FastAPI(
        docs_url="/api/swagger",
        openapi_url="/api/openapi",
        version="1.0.0",
    )

    settings = get_settings()
    bindRoutes(application, settings)
    application.state.settings = settings
    return application


app = getApp()


if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "main:app",
        port=settings_for_application.BACKEND_PORT,
        reload=True,
        reload_dirs=["app"],
        log_level="debug",
        host=settings_for_application.BACKEND_HOST,
    )
