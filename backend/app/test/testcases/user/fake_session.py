# fake_session.py

from contextlib import asynccontextmanager

class FakeSession:
    def __init__(self):
        self.added_objects = []

    # Если используется конструкция "async with session", нужно поддержать асинхронный контекст:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Здесь можно закрыть соединение или просто ничего не делать
        pass

    async def add(self, instance):
        self.added_objects.append(instance)

    async def commit(self):
        # Просто имитируем commit (ничего не делаем)
        pass

    async def refresh(self, instance):
        # Например, имитируем присвоение идентификатора при сохранении
        instance.id = 1

    async def delete(self, instance):
        if instance in self.added_objects:
            self.added_objects.remove(instance)

    async def close(self):
        # Имитация закрытия сессии
        pass

# Поскольку оригинальная функция get_session реализована как асинхронный генератор,
# определим аналогичную фейковую зависимость:
@asynccontextmanager
async def fake_get_session():
    session = FakeSession()
    try:
        yield session
    finally:
        await session.close()
