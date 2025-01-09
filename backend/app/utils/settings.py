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
from app.schemas.settings import EmailUpdateForm, PasswordUpdateForm
from uuid import UUID
async def update_email(id: UUID,updated_password: PasswordUpdateForm, session: AsyncSession) -> bool:
    query = select(User).where(User.id == id)
    result = await session.scalar(query)
    if not result:
        return False
    for key, value in updated_password.model_dump(exclude_none=True).items():
        setattr(result, key, value)
    await session.commit()
    return True
async def update_password(id: UUID, updated_email: EmailUpdateForm, session: AsyncSession) -> bool:
    query = select(User).where(User.id == id)
    result = await session.scalar(query)
    if not result:
        return False
    for key, value in updated_email.model_dump(exclude_none=True).items():
        setattr(result, key, value)
    await session.commit()
    return True