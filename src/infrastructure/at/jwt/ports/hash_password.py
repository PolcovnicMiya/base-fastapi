from abc import ABC, abstractmethod


class HashingPasswordRepositoryPort(ABC):
    @abstractmethod
    async def hash_password(self, password: str) -> str: ...

    @abstractmethod
    async def validate_password(
        self, password: str, hashed_password: bytes
    ) -> bool: ...
