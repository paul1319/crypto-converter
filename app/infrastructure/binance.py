from binance.client import AsyncClient


async def init_binance_client() -> AsyncClient:
    client = await AsyncClient.create()
    yield client
    await client.close_connection()
