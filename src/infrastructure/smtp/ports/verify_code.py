
from abc import ABC, abstractmethod

class VerifyEmailSMTPRepositoryPort(ABC):
    @abstractmethod
    async def send_verify_code(self, to:str, code:str)->None:...