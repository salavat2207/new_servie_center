import aioredis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cache(key: str):
    data = await redis.get(key)
    return json.loads(data) if data else None

async def set_cache(key: str, value, expire: int = 60):
    await redis.set(key, json.dumps(value), ex=expire)