from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from app.config import DefaultSettings, get_settings
from app.database.connection import get_session
from app.database.models import User
from app.database.models import TaskInCalendar
from app.database.models import DeadlineTask
from app.schemas.task import TaskForm



async def create_task(session: AsyncSession, task_and_user_data: TaskForm) -> bool:
    task = DeadlineTask(**task_and_user_data.model_dump(exclude_unset=True))
    session.add(task)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True
