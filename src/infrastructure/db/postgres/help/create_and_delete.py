from src.infrastructure.db.postgres.connection import PostgresDataBaseConnection 
from src.infrastructure.db.postgres.models import Base


async def create_tables():
    async with PostgresDataBaseConnection().async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with PostgresDataBaseConnection().async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
