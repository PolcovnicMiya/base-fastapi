from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.configuration import Environments


POSTGRES_PASS = Environments().pg.POSTGRES_PASS
POSTGRES_HOST = Environments().pg.POSTGRES_HOST
POSTGRES_NAME = Environments().pg.POSTGRES_NAME
POSTGRES_USER = Environments().pg.POSTGRES_USER
POSTGRES_PORT = Environments().pg.POSTGRES_PORT
TEST_DB_PASS = Environments().tpg.TEST_DB_PASS
TEST_DB_HOST = Environments().tpg.TEST_DB_HOST
TEST_DB_NAME = Environments().tpg.TEST_DB_NAME
TEST_DB_USER = Environments().tpg.TEST_DB_USER
TEST_DB_PORT = Environments().tpg.TEST_DB_PORT


@dataclass
class PostgresDataBaseConnection:
    url = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
    )
    test_url = (
        f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@"
        f"{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
    )
    sync_url = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
    )

    echo = False
    echo_pool = False
    pool_size = 5
    max_overflow = 10

    async_engine = create_async_engine(
        url=url,
        echo=echo,
        echo_pool=echo_pool,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
    session_factory = async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        expire_on_commit=False,
    )
    test_async_engine = create_async_engine(
        url=test_url,
        echo=echo,
        echo_pool=echo_pool,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
    test_session_factory = async_sessionmaker(
        bind=test_async_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    sync_engine = create_engine(
        url=sync_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )

    @classmethod
    async def dispose(cls):
        await cls.async_engine.dispose()

    @classmethod
    async def test_dispose(cls):
        await cls.test_async_engine.dispose()

    @classmethod
    async def session_use(cls):
        async with cls.session_factory() as session:
            yield session

    @classmethod
    async def test_session_use(cls):
        async with cls.test_session_factory() as session:
            yield session

# print(postgres_session.url)