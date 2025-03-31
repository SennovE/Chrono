import pytest
pytestmark = [pytest.mark.anyio]
class TestUser:
    async def test_register(self, client):
        res = await client.get('/')