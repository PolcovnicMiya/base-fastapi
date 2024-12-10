from dataclasses import dataclass
from typing import Dict

from src.application.auth.dto import SendRegisterCodeDTO, AcceptRegisterCodeDTO
from src.domain.auth.use_case import SendRegisterCodeUseCase, AcceptRegisterCodeUseCase
from src.infrastructure.db.postgres.ports import (
    RolePostgresRepositoryPort,
    UserPostgresRepositoryPort,
    UserRolePostgresRepositoryPort,
)
from src.infrastructure.db.redis.ports.user_code import EmailCodeRedisRepositoryPort
from src.infrastructure.smtp.ports.verify_code import VerifyEmailSMTPRepositoryPort
from src.application.auth.interfaces.register import RegisterUserServiceInterface


@dataclass(frozen=1, slots=1)
class RegisterUserService(RegisterUserServiceInterface):
    _user_postgres_repo: UserPostgresRepositoryPort
    _email_code_redis_repo: EmailCodeRedisRepositoryPort
    _verify_email_smtp_repo: VerifyEmailSMTPRepositoryPort
    _role_postgres_repo: RolePostgresRepositoryPort
    _user_role_postgres_repo: UserRolePostgresRepositoryPort

    async def send_register_code(self, dto: SendRegisterCodeDTO)-> Dict[str, str]:
        use_case = SendRegisterCodeUseCase(
            _user_postgres_repo = self._user_postgres_repo,
            _email_code_redis_repo = self._email_code_redis_repo,
            _verify_email_smtp_repo = self._verify_email_smtp_repo
            )
        await use_case(dto=dto)

        
    async def accept_register_code(self, dto: AcceptRegisterCodeDTO):
        use_case = AcceptRegisterCodeUseCase(
            _role_postgres_repo = self._role_postgres_repo,
            _user_postgres_repo = self._user_postgres_repo,
            _user_role_postgres_repo = self._user_role_postgres_repo,
            _email_code_redis_repo = self._email_code_redis_repo,
            _verify_email_smtp_repo = self._verify_email_smtp_repo
        )
        await use_case(dto=dto)
