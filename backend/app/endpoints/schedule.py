from fastapi import APIRouter, Depends, Security, status, Body, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.schemas import ScheduleForm, ScheduleResponse
from app.database.models import User
from app.utils.user import get_current_user
from app.utils.schedule import add_schedule_task, get_schedule_tasks

api_router = APIRouter(prefix="/schedule", tags=["Schedule"])


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def new_schedule_task(
    schedule_task: Annotated[ScheduleForm, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> None:
    await add_schedule_task(session, schedule_task, current_user)


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def get_users_tasks(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> list[ScheduleResponse]:
    return await get_schedule_tasks(session, current_user)