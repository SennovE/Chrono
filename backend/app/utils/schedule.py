import asyncio

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from app.schemas import ScheduleForm, ScheduleUpdateForm
from app.database.models import User, Schedule


async def add_schedule_task(
    session: AsyncSession,
    schedule_task_form: ScheduleForm,
    current_user: User
) -> None:
    if (schedule_task_form.start_time.year != schedule_task_form.end_time.year or
        schedule_task_form.start_time.month != schedule_task_form.end_time.month or
        schedule_task_form.start_time.day != schedule_task_form.end_time.day
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task should start and end on the same day",
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
    )
    session.add(schedule_task)
    await session.commit()


async def get_schedule_tasks(session: AsyncSession, current_user: User) -> list[Schedule]:
    query = select(Schedule) \
        .where(Schedule.owner_id == current_user.id) \
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
        if key == "start_time":
            result.year = updated_task.start_time.year
            result.month = updated_task.start_time.month
            result.day = updated_task.start_time.day
            result.start_hours = updated_task.start_time.hour
            result.start_minutes = updated_task.start_time.minute
            result.week_day = updated_task.start_time.weekday()
        elif key == "end_time":
            result.end_hours = updated_task.end_time.hour
            result.end_minutes = updated_task.end_time.minute
        else:
            setattr(result, key, value)
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
