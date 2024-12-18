from dataclasses import dataclass
from typing import Dict
from uuid import uuid4

from src.infrastructure.at.jwt.ports import HashingPasswordRepositoryPort
from src.application.auth.dto import CreateAccessAndRefreshTokenDTO,RefreshAccessTokenDTO
from src.infrastructure.db.postgres.ports import (
    UserPostgresRepositoryPort,
    UserRolePostgresRepositoryPort,
)
from src.infrastructure.db.redis.ports import JWTRedisRepositoryPort
from src.infrastructure.at.jwt.ports.access_and_refresh import (
    AccessAndRefreshJWTRepositoryPort
)
from src.domain.auth.exception import AuthClientException


@dataclass(slots=1)
class CreateAccessAndRefreshTokenUseCase:
    _access_and_refresh_jwt_repo: AccessAndRefreshJWTRepositoryPort
    _user_postgres_repo: UserPostgresRepositoryPort
    _user_role_postgres_repo: UserRolePostgresRepositoryPort
    _jwt_redis_repo: JWTRedisRepositoryPort
    _hashing_password_repo: HashingPasswordRepositoryPort

    async def __call__(self, dto: CreateAccessAndRefreshTokenDTO)->Dict[str, str] | None:
        existing_user = await self._user_postgres_repo.select_one_user_by_email(dto.email)
        if existing_user is None:
            raise AuthClientException(message="User does not Exist!")
        

        if not await self._hashing_password_repo.validate_password(password=dto.password, hashed_password=existing_user["password"].encode('utf-8')):
            raise AuthClientException(message="Invalid password!")
        role_id = await self._user_role_postgres_repo.select_one_user_by_user_id(
            existing_user["id"]
        )
        if role_id is None:
            raise AuthClientException(
                message='Role does not exist!'
            )
        data = {
            "user_id": existing_user["id"],
            "session_id": str(uuid4()),
            "email": existing_user["email"],
            "role_id": role_id["role_id"],
        }
        refresh_token = await self._access_and_refresh_jwt_repo.encode_token(
            token_type="refresh", data=data
        )
        access_token = await self._access_and_refresh_jwt_repo.encode_token(
            token_type="access", data=data
        )
        await self._jwt_redis_repo.set_one_jwt(
            session_id=data["session_id"],
            user_id=data["user_id"],
            email=data["email"],
            token_type='access',
            token=access_token
        )
        await self._jwt_redis_repo.set_one_jwt(
            session_id=data["session_id"],
            user_id=data["user_id"],
            email=data["email"],
            token_type='refresh',
            token=refresh_token
        )
        return {
            'refresh_token': refresh_token,
            'access_token': access_token,
        }


@dataclass(slots=1)
class RefreshAccessTokenUseCase:
    _access_and_refresh_jwt_repo: AccessAndRefreshJWTRepositoryPort
    _user_role_postgres_repo: UserRolePostgresRepositoryPort
    _jwt_redis_repo: JWTRedisRepositoryPort

    async def __call__(self, dto: RefreshAccessTokenDTO)->Dict[str, str] | None:
        decode_token = await self._access_and_refresh_jwt_repo.decode_token(
            token=dto.refresh_token
        )
        if decode_token is None:
            raise AuthClientException(message="Token does not exist!")
        if decode_token["type"] != "refresh":
            raise AuthClientException(message="Invalid token type!")

        token = await self._jwt_redis_repo.get_one_jwt(
            session_id=decode_token["session_id"],
            user_id=decode_token["user_id"],
            email=decode_token["email"],
            token_type=decode_token["type"],
        )

        if token is None:
            raise AuthClientException(message="Does not exist Token!")
        role_id = await self._user_role_postgres_repo.select_one_user_by_user_id(
            user_id=decode_token["user_id"]
        )
        decode_token.pop("exp", None)

        decode_token["role_id"] = role_id["role_id"]

        new_access_token = await self._access_and_refresh_jwt_repo.encode_token(
            token_type="access", data=decode_token
        )
        return {"access_token": new_access_token}
