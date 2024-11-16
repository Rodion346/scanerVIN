from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=True)
