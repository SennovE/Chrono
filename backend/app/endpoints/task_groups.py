from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, Security, Body, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, TaskGroup, UserToGroup, Schedule
from app.schemas import TaskGroupBase, TaskGroupForm, UpdateTaskGroupForm
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
    )
    session.add(group)
    await session.commit()
    await session.refresh(group)
    user_to_group = UserToGroup(
        user_id = current_user.id,
        group_id = group.id,
    )
    session.add(user_to_group)
    await session.commit()



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
    group_id: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> None:
    query = delete(UserToGroup) \
            .where(UserToGroup.user_id == current_user.id, UserToGroup.group_id == group_id)
    await session.execute(query)
    update_query = update(Schedule).where(
        Schedule.group_id == group_id
    ).values(group_id=None)
    await session.execute(update_query)
    await session.commit()


@api_router.get(
    "/all",
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
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> list[TaskGroupForm]:
    query = select(TaskGroup) \
            .join(UserToGroup, TaskGroup.id == UserToGroup.group_id) \
            .where(UserToGroup.user_id == current_user.id)
    result = await session.scalars(query)
    return result.all()


@api_router.post(
    "/add_by_code",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect email or password",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No group with this code",
        },
    },
)
async def add_group_by_code(
    code: Annotated[UUID, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> None:
    query = select(TaskGroup) \
            .join(UserToGroup, TaskGroup.id == UserToGroup.group_id) \
            .where(UserToGroup.user_id == current_user.id, TaskGroup.code == code)
    task_group = await session.scalar(query)
    if task_group is not None:
        return
    query = select(TaskGroup).where(TaskGroup.code == code)
    task_group = await session.scalar(query)
    if task_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No group with this code",
        )
    user_to_group = UserToGroup(
        user_id = current_user.id,
        group_id = task_group.id
    )
    session.add(user_to_group)
    await session.commit()


@api_router.put(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No group with with this ID",
        }
    },
)
async def update_group(
    group: UpdateTaskGroupForm,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Security(get_current_user)],
) -> None:
    query = select(TaskGroup) \
            .join(UserToGroup, TaskGroup.id == UserToGroup.group_id) \
            .where(UserToGroup.user_id == current_user.id, TaskGroup.id == group.id)
    result = await session.scalar(query)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No group with this ID",
        )
    if group.name is not None:
        result.name = group.name
    if group.color is not None:
        result.color = group.color
    await session.commit()
