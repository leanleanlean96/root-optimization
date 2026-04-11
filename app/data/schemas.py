from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(225), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    routes: Mapped[list["Route"]] = relationship(
        "Route",
        back_populates="user",
    )

class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    distance_m: Mapped[float] = mapped_column(nullable=False)
    duration_s: Mapped[float] = mapped_column(nullable=False)
    geometry: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="routes",
    )
