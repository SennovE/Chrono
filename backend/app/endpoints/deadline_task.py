from app.database.models import DeadlineTask
from app.database.connection import get_session
from app.schemas import DeadlineTaskDebugResponse, DeadlineTaskCreateForm

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import APIRouter, Body
from app.utils.user import get_current_user, User


api_router = APIRouter(
    prefix="/deadline_task",
    tags=["Deadline_task"]
)


@api_router.get("/debug/deadline_tasks_table/", response_model=list[DeadlineTaskDebugResponse])
async def get_deadline_tasks_debug(
    session: AsyncSession = Depends(get_session)
) -> list[DeadlineTaskDebugResponse]:
    query = select(DeadlineTask)
    result = await session.scalars(query)
    return result.all()


@api_router.post('/create_deadline_task',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Task creation failed",
        },
    },
    summary="Create a deadline task")
async def create_deadline_task(create_task_form: Annotated[DeadlineTaskCreateForm,  Body()], current_user: Annotated[User, Depends(get_current_user)], session: AsyncSession = Depends(get_session)):
    is_success = await create_deadline_task(session, create_task_form, current_user)
    if is_success:
        return {"message": "Task created"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task not created",
    )
