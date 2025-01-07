
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select
from app.database.models import DeadlineTask
from app.schemas.task import TaskForm

async def create_task(session: AsyncSession, task_and_user_data: TaskForm) -> bool:
    try:
        task = DeadlineTask(**task_and_user_data.model_dump(exclude_unset=True))
    except:
        return False
    session.add(task)
    try:
        await session.commit()
    except:
        return False
    return True
