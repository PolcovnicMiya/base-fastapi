from dataclasses import dataclass
import random

from src.infrastructure.smtp.ports.verify_code import VerifyEmailSMTPRepositoryPort
from src.application.auth.dto.register import SendRegisterCodeDTO, AcceptRegisterCodeDTO
from src.infrastructure.db.postgres.ports import (
    UserPostgresRepositoryPort,
    RolePostgresRepositoryPort,
    UserRolePostgresRepositoryPort,
)
from src.infrastructure.db.redis.ports import (
    EmailCodeRedisRepositoryPort,
    EmailAttemptRedisRepositoryPort,
)
from src.domain.auth.exception import AuthClientException


@dataclass(slots=True)
class SendRegisterCodeUseCase:
    _user_postgres_repo: UserPostgresRepositoryPort
    _email_code_redis_repo: EmailCodeRedisRepositoryPort
    _verify_email_smtp_repo: VerifyEmailSMTPRepositoryPort

    async def __call__(self, dto: SendRegisterCodeDTO) -> None:
        existing_user = await self._user_postgres_repo.select_one_user_by_email(
            email_filter=dto.email
        )
        if existing_user:
            raise AuthClientException(message="Hey bro I know you")
        code = random.randint(99999, 999999)

        await self._verify_email_smtp_repo.send_verify_code(to=dto.email, code=code)

        await self._email_code_redis_repo.set_one_code(email=dto.email, code=code)


@dataclass
class AcceptRegisterCodeUseCase:
    _role_postgres_repo: RolePostgresRepositoryPort
    _user_postgres_repo: UserPostgresRepositoryPort
    _user_role_postgres_repo: UserRolePostgresRepositoryPort
    _email_code_redis_repo: EmailCodeRedisRepositoryPort
    _verify_email_smtp_repo: VerifyEmailSMTPRepositoryPort

    async def __call__(self, dto: AcceptRegisterCodeDTO) -> None:
        existing_user = await self._user_postgres_repo.select_one_user_by_email(
            email_filter=dto.email
        )
        if existing_user:
            raise AuthClientException(message="User already exists!")
        
        existing_code = await self._email_code_redis_repo.get_one_code(email=dto.email)

        if not existing_code:
            raise AuthClientException(message="Verification code not found or expired!")

        if dto.code != existing_code:
            raise AuthClientException(message="Code is invalid")
        user_id = await self._user_postgres_repo.insert_one_user(
            email=dto.email, password=dto.password
        )

        role_id = await self._role_postgres_repo.select_one_role_by_name(name="user")
        
        if not role_id:
            raise AuthClientException(message="Role user does not exist!")
        
        role_user_id = await self._user_role_postgres_repo.insert_user_role(
            user_id=user_id, role_id=role_id["id"]
        )
        print(role_user_id)

        await self._email_code_redis_repo.delete_one_code(email=dto.email)
