from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.database.connection import get_session
from app.utils.task import create_task
from app.schemas.task import TaskForm, TaskInfo 
from app.utils.user import (
    get_current_user,
    User
)
api_router = APIRouter(prefix="/user/task", tags=["Task"])

@api_router.post(
    "/deadline",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Task creation failed",
        },
    },
    summary="Create a deadline task",
)
async def task_creation(
    task_info: Annotated[TaskInfo, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    try:
       
        task_data = task_info.model_dump()
        task_data["user_id"] = current_user.id 
        task_form = TaskForm(**task_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task data",
        )
    
    is_success = await create_task(session, task_form)
    if is_success:
        return {"message": "Task created!"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task creation failed",
    )