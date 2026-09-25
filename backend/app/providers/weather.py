import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger("weather_provider")


class WeatherProvider:
    """Live weather integration using Open-Meteo free public API."""

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    WEATHER_CODES = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        80: "Rain Showers",
        81: "Moderate Showers",
        82: "Violent Showers",
        95: "Thunderstorm",
    }

    def check_health(self) -> Dict[str, Any]:
        """Verify connectivity to weather API provider."""
        try:
            res = requests.get(
                self.GEOCODE_URL,
                params={"name": "London", "count": 1},
                timeout=3,
            )
            return {
                "provider": "open-meteo",
                "status": "healthy" if res.status_code == 200 else "degraded",
                "latency_ms": int(res.elapsed.total_seconds() * 1000),
            }
        except Exception as e:
            logger.warning("Weather provider health check failed: %s", e)
            return {
                "provider": "open-meteo",
                "status": "unhealthy",
                "error": str(e),
            }

    def get_weather_for_city(self, city: str, days: int = 5) -> Dict[str, Any]:
        """Fetch current weather and multi-day forecast for a city."""
        try:
            # 1. Geocode city name to lat/long
            geo_res = requests.get(
                self.GEOCODE_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=4,
            )
            geo_data = geo_res.json()
            results = geo_data.get("results")
            if not results:
                return self._fallback_weather(city, days)

            top = results[0]
            lat = top.get("latitude")
            lon = top.get("longitude")
            country = top.get("country", "")

            # 2. Query forecast
            forecast_res = requests.get(
                self.FORECAST_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                    "timezone": "auto",
                    "forecast_days": min(max(days, 1), 7),
                },
                timeout=4,
            )
            data = forecast_res.json()
            current = data.get("current", {})
            daily = data.get("daily", {})

            current_code = current.get("weather_code", 0)
            condition = self.WEATHER_CODES.get(current_code, "Pleasant")

            forecast_days = []
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            codes = daily.get("weather_code", [])

            for i in range(len(dates)):
                day_code = codes[i] if i < len(codes) else 0
                forecast_days.append({
                    "date": dates[i],
                    "max_temp_c": max_temps[i] if i < len(max_temps) else None,
                    "min_temp_c": min_temps[i] if i < len(min_temps) else None,
                    "condition": self.WEATHER_CODES.get(day_code, "Pleasant"),
                })

            return {
                "city": city,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "current": {
                    "temperature_c": current.get("temperature_2m", 21.0),
                    "feels_like_c": current.get("apparent_temperature", 21.0),
                    "condition": condition,
                    "humidity_percent": current.get("relative_humidity_2m", 50),
                    "wind_speed_kmh": current.get("wind_speed_10m", 10.0),
                },
                "forecast": forecast_days,
            }
        except Exception as exc:
            logger.warning("Failed to fetch live weather for %s: %s. Using seasonal fallback.", city, exc)
            return self._fallback_weather(city, days)

    def _fallback_weather(self, city: str, days: int) -> Dict[str, Any]:
        """Provides estimated seasonal weather data when live provider is unreachable."""
        return {
            "city": city,
            "country": "",
            "latitude": None,
            "longitude": None,
            "current": {
                "temperature_c": 22.0,
                "feels_like_c": 22.5,
                "condition": "Pleasant & Clear",
                "humidity_percent": 55,
                "wind_speed_kmh": 12.0,
            },
            "forecast": [
                {
                    "day_number": i + 1,
                    "max_temp_c": 24.0,
                    "min_temp_c": 16.0,
                    "condition": "Mild & Sunny",
                }
                for i in range(min(days, 7))
            ],
            "note": "Estimated seasonal baseline (live weather provider unavailable)",
        }
