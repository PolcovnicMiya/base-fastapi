import os
from pathlib import Path
from typing import Annotated
from dataclasses import dataclass
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_PASS: str
    POSTGRES_USER: str
    POSTGRES_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_PASS: str
    TEST_DB_USER: str
    TEST_DB_NAME: str

    PUBLIC_KEY_PATH: Path = (
        BASE_DIR / "src" / "infrastructure" / "at" / "jwt" / "keys" / "jwt-public.pem"
    )
    PRIVATE_KEY_PATH: Path = (
        BASE_DIR / "src" / "infrastructure" / "at" / "jwt" / "keys" / "-jwt-private.pem"
    )
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_IN_SECOND: int
    REFRESH_TOKEN_EXPIRE_IN_SECOND: int

    REDIS_USER: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_PORT: int
    SMTP_HOST: str

    EMAIL_CODE_LIFETIME : int
    EMAIL_ATTEMPT_LIFETIME : int


    class Config:
        env_file = ".env"


@dataclass(frozen=1, slots=1)
class Postgres:
    POSTGRES_HOST: str = Settings().POSTGRES_HOST
    POSTGRES_PORT: str = Settings().POSTGRES_PORT
    POSTGRES_PASS: str = Settings().POSTGRES_PASS
    POSTGRES_USER: str = Settings().POSTGRES_USER
    POSTGRES_NAME: str = Settings().POSTGRES_NAME


@dataclass(frozen=1, slots=1)
class Test_Postgres:
    TEST_DB_HOST: str = Settings().TEST_DB_HOST
    TEST_DB_PORT: str = Settings().TEST_DB_PORT
    TEST_DB_PASS: str = Settings().TEST_DB_PASS
    TEST_DB_USER: str = Settings().TEST_DB_USER
    TEST_DB_NAME: str = Settings().TEST_DB_NAME


@dataclass(frozen=1, slots=1)
class JWT_Config:
    PUBLIC_KEY_PATH: Path = Settings().PUBLIC_KEY_PATH
    PRIVATE_KEY_PATH: Path = Settings().PRIVATE_KEY_PATH
    ALGORITHM: str = Settings().ALGORITHM
    ACCESS_TOKEN_EXPIRE_IN_SECOND: str = Settings().ACCESS_TOKEN_EXPIRE_IN_SECOND
    REFRESH_TOKEN_EXPIRE_IN_SECOND: str = Settings().REFRESH_TOKEN_EXPIRE_IN_SECOND


@dataclass(frozen=1, slots=1)
class Redis_Config:
    REDIS_USER: str = Settings().REDIS_USER
    REDIS_HOST: str = Settings().REDIS_HOST
    REDIS_PORT: str = Settings().REDIS_PORT
    REDIS_DB: str = Settings().REDIS_DB


@dataclass(frozen=1, slots=1)
class SMTP_Config:
    SMTP_EMAIL: str = Settings().SMTP_EMAIL
    SMTP_PASSWORD: str = Settings().SMTP_PASSWORD
    SMTP_PORT: int = Settings().SMTP_PORT
    SMTP_HOST: str = Settings().SMTP_HOST

@dataclass(frozen=1, slots=1)
class Email_Code_Config:
    EMAIL_CODE_LIFETIME : int = Settings().EMAIL_CODE_LIFETIME
    EMAIL_ATTEMPT_LIFETIME : int = Settings().EMAIL_ATTEMPT_LIFETIME  


@dataclass(frozen=1, slots=1)
class Environments:
    pg: Postgres = Postgres()
    tpg: Test_Postgres = Test_Postgres()
    jwt_config: JWT_Config = JWT_Config()
    redis_config: Redis_Config = Redis_Config()
    smtp: SMTP_Config = SMTP_Config()
    email_code:Email_Code_Config = Email_Code_Config()

print(Environments().jwt_config.PUBLIC_KEY_PATH)