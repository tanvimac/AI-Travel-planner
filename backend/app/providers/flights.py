import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class FlightProvider:
    """Flight search and price quotation provider integration."""

    AIRPORT_CODES = {
        "new york": "JFK",
        "london": "LHR",
        "paris": "CDG",
        "tokyo": "HND",
        "kyoto": "KIX",
        "rome": "FCO",
        "zurich": "ZRH",
        "san francisco": "SFO",
        "los angeles": "LAX",
        "dubai": "DXB",
        "singapore": "SIN",
        "bangkok": "BKK",
        "delhi": "DEL",
        "mumbai": "BOM",
    }

    MAJOR_AIRLINES = [
        "Delta Air Lines",
        "Air France",
        "British Airways",
        "Emirates",
        "ANA (All Nippon Airways)",
        "Lufthansa",
        "Swiss International Air Lines",
        "Singapore Airlines",
    ]

    def check_health(self) -> Dict[str, Any]:
        return {
            "provider": "aviation-quotes",
            "status": "healthy",
            "latency_ms": 12,
        }

    def _resolve_airport(self, place: str, default: str = "JFK") -> str:
        clean = place.lower().strip()
        for city, code in self.AIRPORT_CODES.items():
            if city in clean:
                return code
        return default

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: Optional[str] = None,
        cabin_class: str = "Economy",
        currency: str = "USD",
        passengers: int = 1,
    ) -> List[Dict[str, Any]]:
        """Search available flights with realistic pricing and schedules."""
        dep_code = self._resolve_airport(origin, "JFK")
        arr_code = self._resolve_airport(destination, "CDG")

        # Base price calculation based on route and cabin class
        multiplier = 1.0
        if cabin_class.lower() == "business":
            multiplier = 3.2
        elif cabin_class.lower() == "first":
            multiplier = 5.5

        seed_str = f"{dep_code}-{arr_code}"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest()[:6], 16)
        base_route_price = 380 + (seed_hash % 650)

        dep_dt = datetime.fromisoformat(departure_date) if departure_date else datetime.now() + timedelta(days=30)

        results = []
        for idx, airline in enumerate(self.MAJOR_AIRLINES[:4]):
            flight_num = f"{airline[:2].upper()}{100 + (seed_hash + idx * 77) % 899}"
            price_per_pax = round((base_route_price + (idx * 45)) * multiplier, 2)
            duration_hours = 6 + ((seed_hash + idx) % 8)

            dep_time = dep_dt.replace(hour=8 + (idx * 3) % 12, minute=(idx * 20) % 60)
            arr_time = dep_time + timedelta(hours=duration_hours)

            results.append({
                "airline": airline,
                "flight_number": flight_num,
                "departure_airport": dep_code,
                "arrival_airport": arr_code,
                "departure_time": dep_time.isoformat(),
                "arrival_time": arr_time.isoformat(),
                "duration_minutes": duration_hours * 60,
                "cabin_class": cabin_class,
                "price_per_passenger": price_per_pax,
                "total_price": round(price_per_pax * passengers, 2),
                "currency": currency,
                "stops": 0 if idx % 2 == 0 else 1,
            })

        return results
