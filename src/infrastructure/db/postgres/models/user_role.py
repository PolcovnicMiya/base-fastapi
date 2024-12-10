from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.postgres.models.base import Base


class UserRole(Base):
    __tablename__ = "user_role"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(column="users.id")
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(column="roles.id")
    )
