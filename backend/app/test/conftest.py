import asyncio
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
import pytest_asyncio
settings = get_settings()

engine = create_async_engine(
    settings.database_uri,
    echo=True,
    future=True,
    pool_size=200,
    max_overflow=0,
)

SessionTesting = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

    
@pytest_asyncio.fixture(name='session')
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTesting() as session:
        yield session
