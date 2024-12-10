from typing import Any, Dict
from sqlalchemy import text
from src.infrastructure.db.postgres.ports import UserRolePostgresRepositoryPort
from src.infrastructure.db.postgres.connection import PostgresDataBaseConnection


class UserRolePostgresRepositoryAdapter(UserRolePostgresRepositoryPort):
    _session_factory = PostgresDataBaseConnection().session_factory()

    async def insert_user_role(self, user_id: int, role_id: int) -> int | None:
        query = text(
            """
        INSERT INTO user_role (user_id , role_id)
        VALUES (:user_id, :role_id)
        RETURNING id
        """
        )
        async with self._session_factory as session:
            result =  await session.execute(query, {'user_id': user_id, 'role_id': role_id})
            user_role_id = result.scalar()
            await session.commit()
            return user_role_id
    
    async def select_one_user_by_user_id(self, user_id)-> Dict[str, Any] | None:
        query = text(
            """
        SELECT * FROM user_role
        WHERE user_id = :user_id
        """
        )
        async with self._session_factory as session:
           result =  await session.execute(query, { "user_id": user_id})
        user_role = result.fetchone()
        await session.commit()
        return user_role._mapping if user_role else None