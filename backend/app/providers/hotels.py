from typing import List, Dict, Any, Optional


class HotelProvider:
    """Lodging and accommodations provider integration."""

    CURATED_HOTELS = {
        "tokyo": [
            {"name": "Aman Tokyo", "tier": "Luxury", "price_per_night": 1200.0, "rating": 4.9, "amenities": ["Spa", "Pool", "Fine Dining", "City Views"]},
            {"name": "Park Hyatt Tokyo", "tier": "Luxury", "price_per_night": 750.0, "rating": 4.8, "amenities": ["Rooftop Bar", "Pool", "Concierge"]},
            {"name": "Hotel Gracery Shinjuku", "tier": "Mid-range", "price_per_night": 160.0, "rating": 4.4, "amenities": ["WiFi", "Godzilla Terrace", "Central Location"]},
            {"name": "Khaosan Tokyo Origami", "tier": "Budget", "price_per_night": 45.0, "rating": 4.2, "amenities": ["Shared Kitchen", "Dorms & Private Rooms"]},
        ],
        "paris": [
            {"name": "Le Bristol Paris", "tier": "Luxury", "price_per_night": 1400.0, "rating": 4.9, "amenities": ["Michelin Dining", "Courtyard Garden", "Spa"]},
            {"name": "Hôtel Plaza Athénée", "tier": "Luxury", "price_per_night": 1100.0, "rating": 4.8, "amenities": ["Eiffel Views", "Dior Spa", "Chic Terrace"]},
            {"name": "CitizenM Paris Champs-Élysées", "tier": "Mid-range", "price_per_night": 220.0, "rating": 4.5, "amenities": ["Mood Lighting", "Rooftop Bar", "High-speed WiFi"]},
            {"name": "Generator Paris", "tier": "Budget", "price_per_night": 55.0, "rating": 4.1, "amenities": ["Rooftop Bar", "Private Rooms & Shared"]},
        ],
        "rome": [
            {"name": "Hotel de Russie", "tier": "Luxury", "price_per_night": 950.0, "rating": 4.8, "amenities": ["Terraced Gardens", "Spa", "Piazza del Popolo Views"]},
            {"name": "Hotel Santa Maria", "tier": "Mid-range", "price_per_night": 210.0, "rating": 4.7, "amenities": ["Orange Garden", "Trastevere", "Free Bikes"]},
            {"name": "The YellowSquare Rome", "tier": "Budget", "price_per_night": 40.0, "rating": 4.3, "amenities": ["Coworking", "Bar", "Social Tours"]},
        ],
        "kyoto": [
            {"name": "The Ritz-Carlton, Kyoto", "tier": "Luxury", "price_per_night": 1100.0, "rating": 4.9, "amenities": ["Kamogawa River Views", "Bonsai", "Michelin Dining"]},
            {"name": "Kyoto Machiya Ryokan", "tier": "Mid-range", "price_per_night": 190.0, "rating": 4.6, "amenities": ["Tatami Rooms", "Garden", "Traditional Tea"]},
            {"name": "Piece Hostel Sanjo", "tier": "Budget", "price_per_night": 35.0, "rating": 4.5, "amenities": ["Cafe", "Terrace", "Modern Design"]},
        ],
        "zurich": [
            {"name": "Baur au Lac", "tier": "Luxury", "price_per_night": 980.0, "rating": 4.9, "amenities": ["Private Park", "Lake Views", "Historic Luxury"]},
            {"name": "25hours Hotel Langstrasse", "tier": "Mid-range", "price_per_night": 240.0, "rating": 4.5, "amenities": ["Sauna", "Restaurant", "Eclectic Design"]},
            {"name": "Zurich Youth Hostel", "tier": "Budget", "price_per_night": 60.0, "rating": 4.3, "amenities": ["Lake Vicinity", "Free Breakfast"]},
        ],
    }

    def check_health(self) -> Dict[str, Any]:
        return {
            "provider": "lodging-inventory",
            "status": "healthy",
            "latency_ms": 10,
        }

    def search_hotels(
        self,
        city: str,
        style: Optional[str] = None,
        max_price: Optional[float] = None,
        currency: str = "USD",
    ) -> List[Dict[str, Any]]:
        """Search hotels matching city and style."""
        key = city.lower().split(",")[0].strip()
        hotels = self.CURATED_HOTELS.get(key)

        if not hotels:
            # Baseline dynamic fallback
            hotels = [
                {"name": f"Grand Palace {city.title()}", "tier": "Luxury", "price_per_night": 450.0, "rating": 4.8, "amenities": ["Spa", "Pool", "Central"]},
                {"name": f"City Center Boutique {city.title()}", "tier": "Mid-range", "price_per_night": 160.0, "rating": 4.5, "amenities": ["WiFi", "Breakfast Included"]},
                {"name": f"Urban Traveler Lodge {city.title()}", "tier": "Budget", "price_per_night": 50.0, "rating": 4.2, "amenities": ["Clean Rooms", "WiFi"]},
            ]

        results = []
        for h in hotels:
            if style and style.lower() in ["luxury", "budget", "mid-range"]:
                if h["tier"].lower() != style.lower():
                    continue
            if max_price and h["price_per_night"] > max_price:
                continue

            item = dict(h)
            item["city"] = city
            item["currency"] = currency
            results.append(item)

        return results or [dict(h, city=city, currency=currency) for h in hotels]
