import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RegistrationForm
from app.database.models.user import User
from app.utils.user import register_user, get_user_by_email

# Список ролей, который повторяется для генерации 30 пользователей
roles = ["admin", "user", "moderator", "guest", "editor"]

# Генерация 30 тестовых наборов данных:
test_users = [
    (
        f"user{i}_{role}@example.com",   # email
        f"user{i}_{role}",                # username
        "password123",                    # password
        role                              # роль (используется только для формирования email/username)
    )
    for i, role in zip(range(30), roles * 6)  # 5 ролей * 6 = 30 пользователей
]

@pytest.mark.asyncio
@pytest.mark.parametrize("email, username, password, role", test_users)
async def test_register_30_users(session: AsyncSession, email: str, username: str, password: str, role: str):
    """
    Тест регистрации 30 пользователей с разными ролями (симулируется через email/username).
    Для каждого набора параметров регистрация должна проходить успешно,
    а пользователь должен появиться в базе данных с ожидаемым username.
    """
    registration_data = RegistrationForm(
        email=email,
        username=username,
        password=password
    )
    success = await register_user(session, registration_data)
    assert success is True, f"Registration failed for {email}"

    user = await get_user_by_email(session, email)
    assert user is not None, f"User not found for {email}"
    assert user.username == username, f"Username mismatch for {email}"
