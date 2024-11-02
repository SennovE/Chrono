from logging import getLogger

from fastapi import FastAPI, Depends
from uvicorn import run

from app.config import DefaultSettings, get_settings
# from app.endpoints import list_of_routes
from schemas import UserCreateForm, UserResponse, UserDebugResponse
from app.db.models import *


from app.db.connection import get_session
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


logger = getLogger(__name__)


# def bindRoutes(application: FastAPI, setting: DefaultSettings) -> None:
#     for route in list_of_routes:
#         application.include_router(route, prefix=setting.PATH_PREFIX)


def getApp() -> FastAPI:
    application = FastAPI(
        docs_url="/api/swagger",
        openapi_url="/api/openapi",
        version="1.0.0",
    )

    settings = get_settings()
    # bindRoutes(application, settings)
    application.state.settings = settings
    return application


app = getApp()


@app.post("/")
async def create_user(user: UserCreateForm, db: AsyncSession = Depends(get_session)):
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()

    return "User created"


@app.get("/debug/get_users/", response_model=List[UserDebugResponse])
async def get_users_debug(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


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
