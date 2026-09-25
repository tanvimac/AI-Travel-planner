from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models.itinerary import Itinerary


class Base(DeclarativeBase):
    pass


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    travelers: Mapped[int] = mapped_column(Integer, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    interests: Mapped[str] = mapped_column(String, nullable=False)
    travel_style: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", server_default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # One-to-many relationship with Itineraries
    itineraries: Mapped[list["Itinerary"]] = relationship(
        "Itinerary",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

