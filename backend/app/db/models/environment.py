from datetime import datetime, date
from typing import Optional, Any
from sqlalchemy import String, Integer, Float, DateTime, Date, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.models.base import Base


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    snapshot_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, index=True)
    temperature_celsius: Mapped[float] = mapped_column(Float, nullable=False)
    feels_like_celsius: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    condition: Mapped[str] = mapped_column(String(100), nullable=False) # Sunny, Rain, Cloudy, Snow, etc.
    humidity_percent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    wind_speed_kmh: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    forecast_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, server_default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
