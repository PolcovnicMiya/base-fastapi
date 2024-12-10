from typing import Any, Dict

from sqlalchemy import text
from src.infrastructure.db.postgres.ports import RolePostgresRepositoryPort
from src.infrastructure.db.postgres.connection import PostgresDataBaseConnection


class RolePostgresRepositoryAdapter(RolePostgresRepositoryPort):
    _session_factory = PostgresDataBaseConnection().session_factory()

    async def insert_one_role(self, name: str) -> int | None:
        query = text(
            """
        INSERT INTO roles (name)
        VALUES (:name)
        RETURNING id
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"name": name})
        role_id = result.scalar()
        return role_id

    async def update_one_role_by_id(self, id_filter: int, name: str) -> None:
        query = text(
            """
        UPDATE roles SET name = :name
        WHERE id = :id_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(
                query, {"name": name, "id_filter": id_filter}
            )

    async def update_one_role_by_name(self, name_filter: int, name: str) -> None:

        query = text(
            """
        UPDATE roles SET name = :name
        WHERE name = :name_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(
                query, {"name": name, "name_filter": name_filter}
            )

    async def select_one_role_by_id(self, role_id: int) -> Dict[str, Any] | None:
        query = text(
            """
        SELECT * FROM roles WHERE id = :role_id
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"role_id": role_id})
            role = result.fetchone()
        return role._mapping if role else None

    async def select_one_role_by_name(self, name: str) -> Dict[str, Any] | None:
        query = text(
            """
            SELECT * FROM roles WHERE name = :name
            """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"name": name})
            role = result.fetchone()
        return role._mapping if role else None
