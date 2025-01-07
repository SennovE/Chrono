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


async def create_deadline_task(session: AsyncSession, task_data: DeadlineTaskCreateForm) -> bool:
    task = DeadlineTask(**task_data.model_dump(exclude_unset=True))
    session.add(task)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True