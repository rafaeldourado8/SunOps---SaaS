import redis.asyncio as aioredis
from app import config

async def get_redis_client():
    """
    Dependência do FastAPI para injetar um cliente Redis assíncrono.
    Decodifica respostas de bytes para strings automaticamente.
    """
    
    try:
        client = await aioredis.from_url(
            f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}",
            encoding="utf-8",
            decode_responses=True # Importante: decodifica respostas para string
        )
        yield client
    finally:
        await client.close()