from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Security, Body, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, TaskGroup
from app.schemas import TaskGroupBase, TaskGroupForm
from app.utils.user import get_current_user
from app.database.connection import get_session

api_router = APIRouter(prefix="/task_groups", tags=["Task Groups"])


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
        },
    },
)
async def add_group(
    group_form: TaskGroupBase,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> None:
    group = TaskGroup(
        name = group_form.name,
        color = group_form.color,
        owner_id = current_user.id,
    )
    session.add(group)
    await session.commit()


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No group with this ID",
        },
    },
)
async def get_group(
    task_id: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[User, Security(get_current_user)],
) -> TaskGroupForm:
    query = select(TaskGroup).where(id = task_id)
    result = await session.scalar(query)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No group with this ID",
        )
    return result


@api_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
        },
    },
)
async def delete_group(
    task_id: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[User, Security(get_current_user)],
) -> None:
    query = delete(TaskGroup).where(id = task_id)
    await session.execute(query)
    await session.commit()


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No group with this ID",
        },
    },
)
async def get_all_groups(
    task_id: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> list[TaskGroupForm]:
    query = select(TaskGroup).where(owner_id = current_user.id)
    result = await session.scalars(query)
    return result.all()
