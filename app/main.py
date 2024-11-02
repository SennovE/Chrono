from logging import getLogger

from fastapi import FastAPI, Depends
from sqlalchemy import Sequence
from uvicorn import run

from app.config import DefaultSettings, get_settings
from app.db.models import User
# from app.endpoints import list_of_routes
from schemas import UserCreateForm, UserResponse, UserDebugResponse
from app.db.models import *


from app.db.connection import get_session
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Coroutine
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


@app.post("/user", response_model=UserResponse)
async def create_user(user: UserCreateForm, db: AsyncSession = Depends(get_session)) -> User:
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


@app.get("/debug/get_users/", response_model=List[UserDebugResponse])
async def get_users_debug(db: AsyncSession = Depends(get_session)) -> Sequence[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
@app.get("/debug/get_users_by_email/", response_model=UserResponse)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_session)) -> User:
    stmt =select(User).where(User.email == email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    return db_user

async def get_user_by_email_fun(email: str, db: AsyncSession = Depends(get_session)) -> User:
    stmt =select(User).where(User.email == email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    return db_user
@app.delete("/user", response_model=UserResponse)
async def delete_user_by_email(email: str, db: AsyncSession = Depends(get_session)) -> User:
    db_user =await get_user_by_email_fun(email, db)
    await db.delete(db_user)
    await db.commit()
    return db_user
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
