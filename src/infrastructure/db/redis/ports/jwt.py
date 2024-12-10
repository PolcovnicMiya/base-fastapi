from abc import ABC, abstractmethod
from uuid import UUID


class JWTRedisRepositoryPort(ABC):
    @abstractmethod
    async def set_one_jwt(
        self, session_id: UUID, user_id: int, email: str, token_type: str, *, token: str
    ) -> None: ...

    @abstractmethod
    async def get_one_jwt(
        self, session_id: UUID, user_id: int, email: str, token_type: str
    ) -> str | None: ...

    @abstractmethod
    async def delete_one_jwt(
        self,session_id:UUID, user_id: int, email: str, token_type: str
    ) -> None: ...

    @abstractmethod
    async def delete_all_jwt(
        self, user_id: int, email: str
    ) -> None: ...