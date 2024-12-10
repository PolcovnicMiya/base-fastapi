from datetime import datetime

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.postgres.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    name: Mapped[str] = mapped_column(String(length=28), nullable=False, unique=True)
