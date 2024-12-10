from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
from src.application.auth.dto import (
    SendRegisterCodeDTO,
    AcceptRegisterCodeDTO
)


@dataclass(frozen=1, slots=1)
class RegisterUserServiceInterface(ABC):
    @abstractmethod
    async def send_register_code(
        self, dto: SendRegisterCodeDTO
    ) -> Dict[str, str]: ...

    @abstractmethod
    async def accept_register_code(
        self, dto: AcceptRegisterCodeDTO
    ) -> Dict[str, str]: ...
