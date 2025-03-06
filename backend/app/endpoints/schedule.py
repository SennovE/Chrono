from fastapi import APIRouter, Depends, Security, status, Body, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database.connection import get_session
from app.schemas import ScheduleForm, ScheduleResponse, ScheduleUpdateForm, ScheduleGenerate
from app.database.models import User, Schedule
from app.utils.user import get_current_user
from app.utils.schedule import (
    add_schedule_task,
    get_schedule_tasks,
    delete_schedule_task,
    change_schedule_task,
    send_schedule
)
from app.utils.ai_generation import schedule_generation

api_router = APIRouter(prefix="/schedule", tags=["Schedule"])


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Task should start and end on the same day",
        },
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
) -> dict[int, list[ScheduleResponse]]:
    result = await get_schedule_tasks(session, current_user)
    tasks_by_weekday = {i: [] for i in range(0, 7)}
    for task in result:
        tasks_by_weekday[task.week_day].append(task)
    return tasks_by_weekday


@api_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def delete_user_task(
    task_id: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[User, Security(get_current_user)],
) -> None:
    await delete_schedule_task(session, task_id)


@api_router.put(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No task with with this ID",
        }
    },
)
async def update_user_task(
    task_id: Annotated[UUID, Body()],
    updated_task: Annotated[ScheduleUpdateForm, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[User, Security(get_current_user)],
) -> None:
    result = await change_schedule_task(session, task_id, updated_task)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task with with this ID",
        )


@api_router.post(
    '/schedule_generation',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "descriprion": "Non authorized"
        }
    }
)
async def ai_generation(
    response: ScheduleGenerate,
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[ScheduleForm]:
    return await schedule_generation(response, current_user)
    

@api_router.post(
    '/send_ai_schedule',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "descriprion": "Non authorized"
        }
    }
)
async def send_ai_schedule(
    tasks: Annotated[list[ScheduleForm], Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    is_success = await send_schedule(tasks, current_user, session)
    if not is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error submit ai gen tasks"
        )
