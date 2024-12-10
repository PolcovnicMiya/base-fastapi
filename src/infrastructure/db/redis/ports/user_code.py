

from abc import ABC, abstractmethod


class EmailCodeRedisRepositoryPort(ABC):
    @abstractmethod
    async def set_one_code(self, email: str , * , code:str)-> None:...

    @abstractmethod
    async def delete_one_code(self, email: str)-> None:...

    @abstractmethod
    async def get_one_code(self, email: str)-> str | None:...
