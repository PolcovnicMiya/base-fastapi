

from abc import ABC, abstractmethod


class EmailAttemptRedisRepositoryPort(ABC):
    @abstractmethod
    async def set_one_attempt(self, email: str , * , time:int )-> None:...

    @abstractmethod
    async def delete_one_attempt(self, email: str)-> None:...

    @abstractmethod
    async def get_one_attempt(self, email: str)-> str | None:...
