from app.database.models import DeadlineTask
from app.database.connection import get_session
from app.schemas import DeadlineTaskDebugResponse, DeadlineTaskCreateForm, \
DeadlineTaskResponse, DeadlineTaksUpdateForm, DeadlineTaskID

from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import APIRouter, Body, Security
from app.utils.user import get_current_user, User
from app.utils.settings import (
    update_email,
    update_password,
)
from app.utils.settings import (
    EmailUpdateForm,
    PasswordUpdateForm,
    )
from uuid import UUID
api_router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)


@api_router.put(
    "/update_password",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def Update_password(
    updated_password: Annotated[PasswordUpdateForm, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Security(get_current_user)],
) -> str:
    result = await update_password(user.id,updated_password, session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task with with this ID",
        )
    return {"message": "Password updated"}
@api_router.put(
    "/update_email",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
    
)
async def Update_email(
    updated_email: Annotated[EmailUpdateForm, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Security(get_current_user)]
) -> str:
    result = await update_email(user.id,updated_email, session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task with with this ID",
        )
    return {"message": "Email updated"}
