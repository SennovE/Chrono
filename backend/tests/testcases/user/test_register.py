import pytest
pytestmark = [pytest.mark.anyio("asyncio")]
class TestUser:
    async def test_register(self, client):
        res = await client.get('/')
        assert res == 0