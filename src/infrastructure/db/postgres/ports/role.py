from abc import ABC, abstractmethod
from typing import Any, Dict


class RolePostgresRepositoryPort(ABC):
    @abstractmethod
    async def insert_one_role(self, name: str) -> int | None: ...

    @abstractmethod
    async def update_one_role_by_id(self, id_filter: int, name: str) -> None: ...

    @abstractmethod
    async def update_one_role_by_name(self, name_filter: int, name: str) -> None: ...

    @abstractmethod
    async def select_one_role_by_id(self, role_id: int) -> Dict[str, Any] | None: ...

    @abstractmethod
    async def select_one_role_by_name(self, name: str) -> Dict[str, Any] | None: ...
