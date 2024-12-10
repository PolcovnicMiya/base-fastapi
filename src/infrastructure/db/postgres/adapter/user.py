from sqlalchemy import text
from src.infrastructure.db.postgres.ports import UserPostgresRepositoryPort
from src.infrastructure.db.postgres.connection import PostgresDataBaseConnection
from typing import Any, Dict


class UserPostgresRepositoryAdapter(UserPostgresRepositoryPort):
    _session_factory = PostgresDataBaseConnection().session_factory()

    async def insert_one_user(self, email: str, password: str) -> None:
        query = text(
            """
        INSERT INTO users (email, password)
        VALUES (:email , :password)
        RETURNING id
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"email": email, "password": password})
            user_id = result.scalar()
            await session.commit()
            return user_id

    async def update_one_user_by_id(
        self, id_filter: int, password: str, email: str, username: str
    ) -> None:
        query = text(
            """
        UPDATE roles SET password = :password, username =:username , email := email
        WHERE id = :id_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(
                query,
                {
                    "id_filter": id_filter,
                    "email": email,
                    "password": password,
                    "username": username,
                },
            )

    async def update_one_user_by_email(
        self, email_filter: str, password: str, email: str, username: str
    ) -> None:
        query = text(
            """
        UPDATE roles SET password = :password, username =:username , email := email
        WHERE email = :email_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(
                query,
                {
                    "email": email,
                    "password": password,
                    "username": username,
                    "email_filter": email_filter,
                },
            )
            await session.commit()

    async def select_one_user_by_id(self, id_filter: int) -> Dict[str, Any] | None:
        query = text(
            """
        SELECT * FROM users WHERE id = :id_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"id_filter": id_filter})
            user = result.fetchone()
            await session.commit()
            return user._mapping if user else None

    async def select_one_user_by_name(self, name_filter: str) -> Dict[str, Any] | None:
        query = text(
            """
        SELECT * FROM users WHERE id = :id_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"name_filter": name_filter})
            user = result.fetchone()
            await session.commit()
            return user._mapping if user else None

    async def select_one_user_by_email(self, email_filter:str)-> Dict[str, Any] | None:
        query = text(
            """
        SELECT * FROM users WHERE email = :email_filter
        """
        )
        async with self._session_factory as session:
            result = await session.execute(query, {"email_filter": email_filter})
            user = result.fetchone()
            await session.commit()
            return user._mapping if user else None
