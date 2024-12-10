from abc import ABC, abstractmethod
from typing import Any, Dict


class UserPostgresRepositoryPort(ABC):
    @abstractmethod
    async def insert_one_user(self, email: str, password: str) -> int | None: ...

    @abstractmethod
    async def update_one_user_by_id(
        self, id_filter: int, password: str, email: str, username: str
    ) -> None: ...

    @abstractmethod
    async def update_one_user_by_email(
        self, email_filter: str, password: str, email: str, username: str
    ) -> None: ...

    @abstractmethod
    async def select_one_user_by_id(self, id_filter: int) -> Dict[str, Any] | None: ...

    @abstractmethod
    async def select_one_user_by_name(
        self, name_filter: str
    ) -> Dict[str, Any] | None: ...

    @abstractmethod
    async def select_one_user_by_email(
        self, email_filter: str
    ) -> Dict[str, Any] | None: ...    
