from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Dict


class AccessAndRefreshJWTRepositoryPort(ABC):
    @abstractmethod
    async def encode_token(
        self, token_type: str, expire_timedelta: timedelta, data: Dict[str, Any]
    ) -> str: ...

    @abstractmethod
    async def decode_token(self, token: str | bytes) -> Dict[str, Any]: ...
