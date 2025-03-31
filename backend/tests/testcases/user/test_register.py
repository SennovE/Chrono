import pytest
from fastapi import status

@pytest.mark.asyncio
class TestUser:
    async def test_register(self, client):
        res = await client.post(
            '/user/register',
            json={
                "email": "your_email@domen.com",
                "username": "string",
                "password": "your_password"
            })
        
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == None
