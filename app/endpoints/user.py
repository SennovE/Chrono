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
from fastapi import APIRouter as api_router

apiRouter = api_router(
    prefix="/user",
    tags=["User"]
)
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any, Coroutine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


logger = getLogger(__name__)


@apiRouter.post("", response_model=UserResponse)
async def create_user(user: UserCreateForm, db: AsyncSession = Depends(get_session)) -> UserResponse:
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_response = UserResponse.model_validate(db_user)

    return user_response


@apiRouter.get("/debug/get_users/", response_model=List[UserResponse])
async def get_users_debug(db: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    users_response = [UserResponse.model_validate(user_) for user_ in users]
    return users_response


@apiRouter.get("/debug/get_users_by_email/", response_model=UserResponse)
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_session)) -> UserResponse:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    user_response = UserResponse.model_validate(db_user)
    return user_response


async def get_user_by_email_fun(email: str, db: AsyncSession = Depends(get_session)) -> UserResponse:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    user_response = UserResponse.model_validate(db_user)

    return user_response


@apiRouter.delete("", response_model=UserResponse)
async def delete_user_by_email(email: str, db: AsyncSession = Depends(get_session)) -> UserResponse:
    db_user = await get_user_by_email_fun(email, db)
    await db.delete(db_user)
    await db.commit()
    user_response = UserResponse.model_validate(db_user)
    return user_response
