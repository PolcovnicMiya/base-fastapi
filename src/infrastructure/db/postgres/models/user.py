from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(length=255), unique=True, nullable=True
    )
    password: Mapped[str] = mapped_column(
        String(length=255),  nullable=True
    )
    email: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=True)
