
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select
from app.database.models import DeadlineTask
from app.schemas.task import TaskForm
from fastapi import HTTPException, status

async def create_task(session: AsyncSession, task_and_user_data: TaskForm) -> bool:
    task = DeadlineTask(**task_and_user_data.model_dump(exclude_unset=True))
    session.add(task)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database error: {str(e)}"
        )

    return True
