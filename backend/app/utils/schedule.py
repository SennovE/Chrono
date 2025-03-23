import asyncio

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from uuid import UUID

from app.schemas import ScheduleForm, ScheduleUpdateForm
from app.database.models import User, Schedule, TaskGroup


async def check_if_group_exists(group_id: UUID, session: AsyncSession) -> bool:
    if group_id is not None:
        query = select(TaskGroup).where(TaskGroup.id == group_id)
        result = await session.scalar(query)
        if result is None:
            return False
    return True


async def add_schedule_task(
    session: AsyncSession,
    schedule_task_form: ScheduleForm,
    current_user: User
) -> None:
    if (
        schedule_task_form.start_time.year != schedule_task_form.end_time.year or
        schedule_task_form.start_time.month != schedule_task_form.end_time.month or
        schedule_task_form.start_time.day != schedule_task_form.end_time.day
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task should start and end on the same day",
        )
    if not await check_if_group_exists(schedule_task_form.group_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No group with this ID",
        )
    schedule_task = Schedule(
        name = schedule_task_form.name,
        text = schedule_task_form.text,
        year = schedule_task_form.start_time.year,
        month = schedule_task_form.start_time.month,
        day = schedule_task_form.start_time.day,
        start_hours = schedule_task_form.start_time.hour,
        start_minutes = schedule_task_form.start_time.minute,
        end_hours = schedule_task_form.end_time.hour,
        end_minutes = schedule_task_form.end_time.minute,
        recurring = schedule_task_form.recurring,
        week_day = schedule_task_form.start_time.weekday(),
        owner_id = current_user.id,
        group_id = schedule_task_form.group_id
    )
    session.add(schedule_task)
    await session.commit()


async def get_schedule_tasks(session: AsyncSession, current_user: User) -> list[Schedule]:
    query = select(Schedule) \
        .where(Schedule.owner_id == current_user.id) \
        .options(joinedload(Schedule.task_group))\
        .order_by(-((Schedule.end_hours - Schedule.start_hours) * 60 + (Schedule.end_minutes - Schedule.start_minutes)))
    result = await session.scalars(query)
    return result.all()


async def delete_schedule_task(session: AsyncSession, task_id: UUID) -> None:
    query = delete(Schedule).where(Schedule.id == task_id)
    await session.execute(query)
    await session.commit()


async def change_schedule_task(
    session: AsyncSession,
    task_id: UUID,
    updated_task: ScheduleUpdateForm,
) -> bool:
    query = select(Schedule).where(Schedule.id == task_id)
    result = await session.scalar(query)
    if not result:
        return False
    for key, value in updated_task.model_dump(exclude_none=True).items():
        if key == "group_id":
            if value == UUID(int=0):
                result.group_id = None
            elif not await check_if_group_exists(value, session):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No group with this ID",
                )
            else:
                result.group_id = value
        elif key == "start_time":
            result.year = value.year
            result.month = value.month
            result.day = value.day
            result.start_hours = value.hour
            result.start_minutes = value.minute
            result.week_day = value.weekday()
        elif key == "end_time":
            result.end_hours = value.hour
            result.end_minutes = value.minute
        else:
            setattr(result, key, value)
    if (result.start_hours > result.end_hours or
        result.start_hours == result.end_hours and result.start_minutes > result.end_minutes):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task should start and end on the same day",
        )
    await session.commit()
    return True


async def send_schedule(
    tasks: list[ScheduleForm],
    current_user: User,
    session: AsyncSession
) -> bool:
    async_tasks = []
    for task in tasks:
        async_tasks.append(add_schedule_task(task, session, current_user))
    await asyncio.gather(*async_tasks)
    return True
