from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from app.config import DefaultSettings, get_settings
from app.database.connection import get_session
from app.database.models import DeadlineTask
from app.schemas import DeadlineTaskCreateForm, TokenData
from app.utils.user import User


async def make_deadline_task(session: AsyncSession, task_data: DeadlineTaskCreateForm, user: User) -> bool:
    task_data = task_data.model_dump()
    task_data["author_id"] = user.id
    task_data["author"] = user.username
    task_data["status"] = 0
    task = DeadlineTask(**task_data)

    session.add(task)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def get_deadline_tasks(session: AsyncSession, current_user : User) \
    -> list[DeadlineTask]:
    query = select(DeadlineTask).where(DeadlineTask.author_id == current_user.id)\
        .order_by(DeadlineTask.deadline_time)
    result = await session.scalars(query)
    return result.all()