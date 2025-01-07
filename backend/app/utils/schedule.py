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
    schedule_task = Schedule(
        **schedule_task_form.model_dump(),
        week_day = schedule_task_form.start_time.weekday(),
        owner_id=current_user.id
    )
    session.add(schedule_task)
    await session.commit()


async def get_schedule_tasks(session: AsyncSession, current_user: User) -> list[Schedule]:
    query = select(Schedule).where(Schedule.owner_id == current_user.id)
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
        setattr(result, key, value)
    await session.commit()
    return True