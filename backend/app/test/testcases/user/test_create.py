import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User
from fastapi import APIRouter, Depends
from app.test.conftest import *
@pytest.mark.asyncio
async def test_users(session: AsyncSession):
    query = select(User)
    result = await session.scalars(query)
    users = result.all()
    print(users)

