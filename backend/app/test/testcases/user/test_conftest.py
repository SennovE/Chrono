# conftest.py
import asyncio
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """
    Фикстура, которая создаёт event loop для всех тестов.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
