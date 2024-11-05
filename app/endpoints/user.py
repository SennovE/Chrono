from logging import getLogger

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy import Sequence
from uvicorn import run
from sqlalchemy.exc import SQLAlchemyError
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
    try:
        async with db.begin():
            db_user = User(email=user.email, hashed_password=hash_password(user.password))
            stmt = select(User).where(User.email == db_user.email)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с таким email уже существует",
                )
            db.add(db_user)
            await db.flush() #commit без commit(что бы могло откатить)
            await db.refresh(db_user)

            user_response = UserResponse.model_validate(db_user)

        return user_response
    except HTTPException as e:
        logger.error(f"Ошибка при добавление пользователя: {e.detail}")
        raise e


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
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_CONFLICT,
            detail="Пользователь не найден",
        )
    user_response = UserResponse.model_validate(db_user)
    return user_response


async def get_user_by_email_fun(email: str, db: AsyncSession = Depends(get_session)) -> User | None:
    stmt = select(User).where(User.email == email)

    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()


    return db_user


@apiRouter.delete("", response_model=UserResponse)
async def delete_user_by_email(email: str, db: AsyncSession = Depends(get_session)) -> UserResponse:
    try:
        async with db.begin():
            db_user = await get_user_by_email_fun(email, db)
            if db_user is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь не найден",
                )
            await db.delete(db_user)
        user_response = UserResponse.model_validate(db_user)
        return user_response
    except HTTPException as e:
        logger.error(f"Ошибка при удалении пользователя: {e.detail}")
        raise e

