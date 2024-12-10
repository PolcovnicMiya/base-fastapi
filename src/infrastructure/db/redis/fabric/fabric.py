import redis.asyncio as aioredis
from src.configuration.setting import Environments

class RedisFabric:
    REDIS_HOST = Environments().redis_config.REDIS_HOST
    REDIS_PORT = Environments().redis_config.REDIS_PORT
    REDIS_DB = Environments().redis_config.REDIS_DB
    REDIS_USER = Environments().redis_config.REDIS_USER
    
    # async_redis_URL = f"redis://{REDIS_USER}:{REDIS_PASS}:{REDIS_PORT}/{REDIS_DB}"

    async_redis_URL = "redis://localhost:6379"

    async_redis_conn = aioredis.from_url(async_redis_URL)

