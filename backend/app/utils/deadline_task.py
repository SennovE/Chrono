from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select, delete

from uuid import UUID
from app.database.models import DeadlineTask
from app.schemas import DeadlineTaskCreateForm, TokenData, \
    DeadlineTaskID, DeadlineTaksUpdateForm
from app.utils.user import User


async def make_deadline_task(session: AsyncSession, task_data: DeadlineTaskCreateForm, user: User) -> bool:
    task_data = task_data.model_dump()
    task_data["author_id"] = user.id
    task_data["author"] = user.username
    task_data["status"] = 0
    task = DeadlineTask(**task_data)

    session.add(task)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def get_deadline_tasks(session: AsyncSession, current_user : User) \
    -> list[DeadlineTask]:
    query = select(DeadlineTask).where(DeadlineTask.author_id == current_user.id)\
        .order_by(DeadlineTask.deadline_time)
    result = await session.scalars(query)
    return result.all()


async def delete_deadline_task(session: AsyncSession, task_data: DeadlineTaskID, current_user: User) -> bool:
    query = select(DeadlineTask).where(DeadlineTask.id == task_data.id)
    task = await session.scalar(query)

    if (current_user.id != task.author_id):
        return False
    
    query = delete(DeadlineTask).where(DeadlineTask.id == task_data.id)
    await session.execute(query)
    await session.commit()
    return True


async def complete_deadline_task(task: DeadlineTaskID, session: AsyncSession) -> bool:
    query = select(DeadlineTask).where(DeadlineTask.id == task.id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    '''if (task.author_id != current_user.id):
        raise HTTPException(status_code=404, detail="You can't change this task")'''

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = 1  
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    return True


async def update_deadline_task(updated_task: DeadlineTaksUpdateForm, session: AsyncSession) -> bool:
    query = select(DeadlineTask).where(DeadlineTask.id == updated_task.id)
    result = await session.scalar(query)
    if not result:
        return False
    for key, value in updated_task.model_dump(exclude_none=True).items():
        setattr(result, key, value)
    await session.commit()
    return True
