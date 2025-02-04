from app.database.models import DeadlineTask
from app.database.connection import get_session
from app.schemas import DeadlineTaskDebugResponse, DeadlineTaskCreateForm, \
DeadlineTaskResponse, DeadlineTaksUpdateForm, DeadlineTaskID, DeadlineGenerate


from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import APIRouter, Body, Security
from app.utils.user import get_current_user, User
from app.utils.deadline_task import (
    make_deadline_task,
    get_deadline_tasks, 
    delete_deadline_task,
    complete_deadline_task,
    update_deadline_task,
    return_deadline_task,
    )
from app.utils.ai_generation import generate_deadline, submit_ai_gen
from uuid import UUID
from typing import List


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
async def create_deadline_task(create_task_form: Annotated[DeadlineTaskCreateForm,  Body()], \
                               current_user: Annotated[User, Depends(get_current_user)],\
                                  session: AsyncSession = Security(get_session)):
    is_success = await make_deadline_task(session, create_task_form, current_user)
    if is_success:
        return {"message": "Task created"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task not created",
    )


@api_router.get(
    "/get_tasks",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def get_user_tasks(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)]
) -> list[DeadlineTaskResponse]:
    result = await get_deadline_tasks(session, current_user)
    return result


@api_router.get(
    "/get_tasks_debug",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def get_user_tasks_debug(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)]
) -> list[DeadlineTaskDebugResponse]:
    result = await get_deadline_tasks(session, current_user)
    return result


@api_router.post(
    "/delete_task",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def delete_user_task(
        task_data: Annotated[DeadlineTaskID, Body()],
        current_user: Annotated[User, Depends(get_current_user)],\
        session: AsyncSession = Security(get_session)) -> None:
    is_success = await delete_deadline_task(session, task_data, current_user)
    if is_success:
        return {"message": "Task deleted"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Delete task error",
    )


@api_router.post(
    "/complete_task",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def complete_task(task: Annotated[DeadlineTaskID, Body()],\
                        session: Annotated[AsyncSession, Depends(get_session)])-> None:
    is_success = await complete_deadline_task(task, session)
    if is_success:
        return {"message": "Task completed"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Complete task error",
    )


@api_router.put(
    "/update_task",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def update_task(task: Annotated[DeadlineTaksUpdateForm, Body()],\
                        session: Annotated[AsyncSession, Depends(get_session)]) -> None:
    is_success = await update_deadline_task(task, session)
    if is_success:
        return {"message": "Task updated"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Update task error",
    )


@api_router.post(
    "/return_to_active",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        }
    },
)
async def return_to_active(task: Annotated[DeadlineTaskID, Body()],\
                        session: Annotated[AsyncSession, Depends(get_session)])-> None:
    is_success = await return_deadline_task(task, session)
    if is_success:
        return {"message": "Task returned to active"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Return to active task error",
    )


@api_router.post('/ai_generation',
                 status_code=status.HTTP_200_OK,
                 responses={
                     status.HTTP_401_UNAUTHORIZED: {
                         "descriprion": "Non authorized"
                     }
                 })
async def ai_generation(response: DeadlineGenerate, \
                        current_user: Annotated[User, Depends(get_current_user)]):
    return await generate_deadline(response, current_user)
    

@api_router.post('/submit_ai_generation',
            status_code=status.HTTP_200_OK,
            responses={
                     status.HTTP_401_UNAUTHORIZED: {
                         "descriprion": "Non authorized"
                     }
                 })
async def submit_ai_generation(tasks: Annotated[list[DeadlineTaskCreateForm], Body()], \
                               current_user: Annotated[User, Depends(get_current_user)],
                               session: Annotated[AsyncSession, Depends(get_session)]):
    is_success = await submit_ai_gen(tasks, current_user, session)

    if (is_success):
        return {"message" : "Submit ai gen tasks"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, \
                        detail="Error submit ai gen tasks")