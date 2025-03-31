import pytest

class TestUser:
    async def test_register(client):
        res = await client.get('/')
        assert res == 0