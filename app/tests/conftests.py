# tests/conftest.py

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import DeclarativeBase
from app.db.connection import get_session
from app.main import app
from app.config.default import DefaultSettings


# Формируем URI для тестовой базы данных
TEST_DATABASE_URI = DefaultSettings.database_uri()

# Создание асинхронного движка
engine = create_async_engine(
    TEST_DATABASE_URI,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URI else {},
    poolclass=StaticPool if "sqlite" in TEST_DATABASE_URI else None,
)

# Создание фабрики сессий
TestingSessionLocal = get_session()

@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """
    Создаёт тестовую базу данных перед запуском тестов и удаляет её после завершения.
    """
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.drop_all)

@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        async with session.begin():
            yield session


@pytest.fixture
async def client(db_session: AsyncSession):
    """
    Предоставляет AsyncClient с переопределённой зависимостью get_db.
    """
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_session()] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
