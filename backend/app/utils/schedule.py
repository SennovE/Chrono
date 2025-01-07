from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import ScheduleForm
from app.database.models import User, Schedule


async def add_schedule_task(session: AsyncSession, schedule_task_form: ScheduleForm, current_user: User):
    schedule_task = Schedule(
        **schedule_task_form.model_dump(),
        week_day = schedule_task_form.start_time.weekday(),
        owner_id=current_user.id
    )
    session.add(schedule_task)
    await session.commit()


async def get_schedule_tasks(session: AsyncSession, current_user: User):
    query = select(Schedule).where(Schedule.owner_id == current_user.id)
    result = await session.scalars(query)
    return result.all()