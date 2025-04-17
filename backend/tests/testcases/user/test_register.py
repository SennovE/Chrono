from app.database.models.user import User
import pytest
from sqlalchemy import select
pytestmark = [pytest.mark.anyio("asyncio")]
class TestUser:
    async def test_register(self, client):
        res = await client.get("/user/debug/users_table/")
        assert res.status_code == 200
        assert res.json() == []
    async def test_successful_registration(self, client, db_session):
        payload = {
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "s3cr3tpassword"
        }
        response = await client.post("/user/register", json=payload)
        assert response.status_code == 200
        saved = await db_session.execute(
            select(User).where(User.username == "charlie")
        )
        user = saved.scalar_one_or_none()
        assert user is not None
        assert user.email == "charlie@example.com"
        assert user.hashed_password != payload["password"]