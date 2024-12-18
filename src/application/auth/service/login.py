from typing import Dict
from src.application.auth.interfaces import LoginUserServiceInterface
from src.application.auth.dto import (
    CreateAccessAndRefreshTokenDTO,
    RefreshAccessTokenDTO,
)
from src.infrastructure.db.postgres.ports import (
    UserPostgresRepositoryPort,
    UserRolePostgresRepositoryPort,
)
from src.infrastructure.db.redis.ports import JWTRedisRepositoryPort
from src.infrastructure.at.jwt.ports import (
    AccessAndRefreshJWTRepositoryPort,HashingPasswordRepositoryPort
)
from src.domain.auth.use_case import (
    CreateAccessAndRefreshTokenUseCase,
    RefreshAccessTokenUseCase,
)


from dataclasses import dataclass


@dataclass(frozen=1, slots=1)
class LoginUserService(LoginUserServiceInterface):
    _access_and_refresh_jwt_repo: AccessAndRefreshJWTRepositoryPort
    _user_postgres_repo: UserPostgresRepositoryPort
    _user_role_postgres_repo: UserRolePostgresRepositoryPort
    _jwt_redis_repo: JWTRedisRepositoryPort
    _hashing_password_repo: HashingPasswordRepositoryPort

    async def create_access_and_refresh_token(
        self, dto: CreateAccessAndRefreshTokenDTO
    ) -> Dict[str, str]:
        use_case = CreateAccessAndRefreshTokenUseCase(
            _access_and_refresh_jwt_repo=self._access_and_refresh_jwt_repo,
            _user_postgres_repo=self._user_postgres_repo,
            _user_role_postgres_repo=self._user_role_postgres_repo,
            _jwt_redis_repo=self._jwt_redis_repo,
            _hashing_password_repo = self._hashing_password_repo
        )
        return await use_case(dto=dto)

    async def refresh_access_token(self, dto: RefreshAccessTokenDTO) -> Dict[str, str]:
        use_case = RefreshAccessTokenUseCase(
            _access_and_refresh_jwt_repo=self._access_and_refresh_jwt_repo,
            _user_role_postgres_repo=self._user_role_postgres_repo,
            _jwt_redis_repo=self._jwt_redis_repo,
        )
        return await use_case(dto=dto)
