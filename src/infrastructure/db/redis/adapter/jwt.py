from uuid import UUID
from src.configuration.setting import Environments
from src.infrastructure.db.redis.fabric import RedisFabric
from src.infrastructure.db.redis.ports import JWTRedisRepositoryPort


class JWTRedisRepositoryAdapter(JWTRedisRepositoryPort):
    _connection = RedisFabric().async_redis_conn

    async def set_one_jwt(
        self, session_id: UUID, user_id: int, email: str, token_type: str, *, token: str
    ) -> None:
        key = f"{session_id}{user_id}{email}{token_type}"
        value = token
        ex = None
        if token_type == "access":
            ex = Environments().jwt_config.ACCESS_TOKEN_EXPIRE_IN_SECOND
        if token_type == "refresh":
            ex = Environments().jwt_config.REFRESH_TOKEN_EXPIRE_IN_SECOND
        await self._connection.set(name=key, value=value, ex=ex)

    async def get_one_jwt(
        self, session_id: UUID, user_id: int, email: str, token_type: str
    ) -> str | None:
        key = f"{session_id}{user_id}{email}{token_type}"
        res = await self._connection.get(name=key)
        if res:
            return res.decode("utf-8")
        return None

    async def delete_one_jwt(
        self, session_id: UUID, user_id: int, email: str, token_type: str
    ) -> None:
        key = f"{session_id}{user_id}{email}{token_type}"
        self._connection.delete(name=key)

    async def delete_all_jwt(self, user_id: int, email: str) -> None:
        key = f"{user_id}{email}"
        await self._connection.delete(key)
