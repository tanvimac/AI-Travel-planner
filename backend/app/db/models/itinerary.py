from datetime import datetime, date
from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Float, DateTime, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.trip import Trip


class Itinerary(Base):
    """Overall synthesized itinerary document (JSONB and Markdown format)."""
    __tablename__ = "itineraries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    itinerary_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
    )
    raw_markdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationship back to Trip
    trip: Mapped["Trip"] = relationship("Trip", back_populates="itineraries")


class ItineraryDay(Base):
    """Discrete single-day entity for structured calendar and day-by-day manipulation."""
    __tablename__ = "itinerary_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    theme: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    trip: Mapped["Trip"] = relationship("Trip", back_populates="itinerary_days")
    items: Mapped[list["ItineraryItem"]] = relationship(
        "ItineraryItem",
        back_populates="day",
        cascade="all, delete-orphan",
        order_by="ItineraryItem.order_index",
        lazy="selectin"
    )


class ItineraryItem(Base):
    """Granular schedule activity item inside an ItineraryDay."""
    __tablename__ = "itinerary_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    itinerary_day_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("itinerary_days.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    time_slot: Mapped[str] = mapped_column(
        String(50), default="morning", server_default="morning", nullable=False
    ) # morning, afternoon, evening, night
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_cost: Mapped[float] = mapped_column(Float, default=0.0, server_default="0.0", nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", server_default="USD", nullable=False)
    item_type: Mapped[str] = mapped_column(
        String(50), default="sightseeing", server_default="sightseeing", nullable=False
    ) # sightseeing, dining, transit, lodging, leisure
    order_index: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    day: Mapped["ItineraryDay"] = relationship("ItineraryDay", back_populates="items")
