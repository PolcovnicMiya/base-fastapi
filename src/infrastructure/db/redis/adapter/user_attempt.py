
from typing import Annotated
from src.configuration.setting import Environments
from src.infrastructure.db.redis.fabric import RedisFabric
from src.infrastructure.db.redis.ports.user_attempt import EmailAttemptRedisRepositoryPort

class EmailAttemptRedisRepositoryAdapter(EmailAttemptRedisRepositoryPort):
    _redis = RedisFabric().async_redis_conn
    async def set_one_attempt(self, email: str , * , time:int ) -> None:
        key = email
        value = time
        await self._redis.set(
            name=key,
            value=value,
            ex=Environments().email_code.EMAIL_ATTEMPT_LIFETIME
        )

    async def delete_one_attempt(self, email: str)-> None:
        key = email
        await self._redis.delete(key)

    async def get_one_attempt(self, email: str)-> str | None:
        key = email
        res = await self._redis.get(key)
        if res: 
            return res.decode("utf-8")
        return None
