from datetime import datetime
from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Date, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.itinerary import Itinerary, ItineraryDay
    from app.db.models.finance import Budget, Expense
    from app.db.models.travel import Flight, Reservation


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    travelers: Mapped[int] = mapped_column(Integer, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", server_default="USD", nullable=False)
    interests: Mapped[str] = mapped_column(String, nullable=False)
    travel_style: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="pending", server_default="pending", nullable=False, index=True
    )
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="trips")
    itineraries: Mapped[list["Itinerary"]] = relationship(
        "Itinerary",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    itinerary_days: Mapped[list["ItineraryDay"]] = relationship(
        "ItineraryDay",
        back_populates="trip",
        cascade="all, delete-orphan",
        order_by="ItineraryDay.day_number",
        lazy="selectin",
    )
    travelers_list: Mapped[list["Traveler"]] = relationship(
        "Traveler",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    destinations_list: Mapped[list["Destination"]] = relationship(
        "Destination",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    budget_record: Mapped[Optional["Budget"]] = relationship(
        "Budget",
        back_populates="trip",
        uselist=False,
        cascade="all, delete-orphan",
    )
    expenses: Mapped[list["Expense"]] = relationship(
        "Expense",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    events: Mapped[list["TripEvent"]] = relationship(
        "TripEvent",
        back_populates="trip",
        cascade="all, delete-orphan",
        order_by="TripEvent.created_at.desc()",
        lazy="selectin",
    )
    flights: Mapped[list["Flight"]] = relationship(
        "Flight",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    reservations: Mapped[list["Reservation"]] = relationship(
        "Reservation",
        back_populates="trip",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Traveler(Base):
    __tablename__ = "travelers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="traveler", server_default="traveler", nullable=False)
    dietary_preferences: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    trip: Mapped["Trip"] = relationship("Trip", back_populates="travelers_list")


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    trip: Mapped[Optional["Trip"]] = relationship("Trip", back_populates="destinations_list")


class TripEvent(Base):
    __tablename__ = "trip_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    event_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, server_default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    trip: Mapped["Trip"] = relationship("Trip", back_populates="events")
