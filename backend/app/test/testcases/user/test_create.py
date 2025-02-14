import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User

@pytest.mark.asyncio
async def test_query_users(session: AsyncSession):
    query = select(User)
    result = await session.scalars(query)
    users = result.all()
    print(users)

