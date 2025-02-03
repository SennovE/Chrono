import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_create_user():
    # Данные для создания пользователя (формат payload зависит от вашей схемы UserCreate)
    payload = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "strongpassword"
    }
    
    # Отправляем POST-запрос на правильный эндпоинт
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/user/register", json=payload)
    
    # Проверяем, что статус ответа 200 (ОК)
    assert response.status_code == 200, f"Ответ: {response.status_code}, тело: {response.text}"
    
    data = response.json()
    
    # Пример проверок. Корректируйте их в соответствии с тем, что возвращает ваш эндпоинт.
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    # Например, если после регистрации пользователь получает id:
    assert "id" in data
