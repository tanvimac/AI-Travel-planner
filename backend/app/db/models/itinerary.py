from datetime import datetime
from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.trip import Base

if TYPE_CHECKING:
    from app.db.models.trip import Trip


class Itinerary(Base):
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
