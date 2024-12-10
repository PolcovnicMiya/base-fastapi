from abc import ABC, abstractmethod
from typing import Any, Dict


class UserRolePostgresRepositoryPort(ABC):
    @abstractmethod
    async def insert_user_role(self, user_id: int, role_id: int) -> int | None: ...

    @abstractmethod
    async def select_one_user_by_user_id(
        self, user_id: int
    ) -> Dict[str, Any] | None: ...
