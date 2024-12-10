from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
from src.application.auth.dto import (
    CreateAccessAndRefreshTokenDTO,
    RefreshAccessTokenDTO,
)


@dataclass(frozen=1, slots=1)
class LoginUserServiceInterface(ABC):
    @abstractmethod
    async def create_access_and_refresh_token(
        self, dto: CreateAccessAndRefreshTokenDTO
    ) -> Dict[str, str]: ...

    @abstractmethod
    async def refresh_access_token(
        self, dto: RefreshAccessTokenDTO
    ) -> Dict[str, str]: ...
