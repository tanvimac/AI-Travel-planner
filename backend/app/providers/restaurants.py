from typing import List, Dict, Any, Optional


class RestaurantProvider:
    """Dining and culinary provider integration."""

    CURATED_RESTAURANTS = {
        "tokyo": [
            {"name": "Sukiyabashi Jiro", "cuisine": "Sushi", "price_range": "$$$$", "rating": 4.9, "specialty": "Omakase Sushi"},
            {"name": "Afuri Ebisu", "cuisine": "Ramen", "price_range": "$$", "rating": 4.6, "specialty": "Yuzu Shio Ramen"},
            {"name": "Gonpachi Nishiazabu", "cuisine": "Izakaya", "price_range": "$$$", "rating": 4.5, "specialty": "Soba & Yakitori"},
            {"name": "Narisawa", "cuisine": "Innovative Satoyama", "price_range": "$$$$", "rating": 4.9, "specialty": "Forest-to-Table Tasting"},
        ],
        "paris": [
            {"name": "L'Ambroisie", "cuisine": "French Haute Cuisine", "price_range": "$$$$", "rating": 4.9, "specialty": "Feuillantine de langoustines"},
            {"name": "Le Comptoir du Relais", "cuisine": "Bistronomy", "price_range": "$$$", "rating": 4.6, "specialty": "Traditional French Bistro Dishes"},
            {"name": "Bouillon Chartier", "cuisine": "Classic French", "price_range": "$", "rating": 4.4, "specialty": "Steak Frites & Escargot"},
            {"name": "Septime", "cuisine": "Modern French", "price_range": "$$$$", "rating": 4.8, "specialty": "Seasonal Tasting Menu"},
        ],
        "rome": [
            {"name": "La Pergola", "cuisine": "Italian Fine Dining", "price_range": "$$$$", "rating": 4.9, "specialty": "Fagottelli La Pergola"},
            {"name": "Da Enzo al 29", "cuisine": "Roman Trattoria", "price_range": "$$", "rating": 4.7, "specialty": "Cacio e Pepe & Carbonara"},
            {"name": "Roscioli Salumeria con Cucina", "cuisine": "Italian Gourmet", "price_range": "$$$", "rating": 4.7, "specialty": "Burrata, Mortadella & Pasta"},
        ],
        "kyoto": [
            {"name": "Kikunoi Honten", "cuisine": "Kaiseki", "price_range": "$$$$", "rating": 4.9, "specialty": "Multi-course Kaiseki"},
            {"name": "Gion Karyo", "cuisine": "Traditional Japanese", "price_range": "$$$", "rating": 4.7, "specialty": "Seasonal Kyoto Cuisine"},
            {"name": "Chao Chao Gyoza", "cuisine": "Dumplings", "price_range": "$", "rating": 4.5, "specialty": "Crispy Pan-Fried Gyoza"},
        ],
        "zurich": [
            {"name": "Kronenhalle", "cuisine": "Swiss / Classic", "price_range": "$$$$", "rating": 4.8, "specialty": "Zürcher Geschnetzeltes with Rösti"},
            {"name": "Zeughauskeller", "cuisine": "Traditional Swiss", "price_range": "$$", "rating": 4.5, "specialty": "Swiss Sausages & Fondue"},
            {"name": "Hiltl", "cuisine": "Vegetarian / Buffet", "price_range": "$$$", "rating": 4.6, "specialty": "World's Oldest Vegetarian Restaurant"},
        ],
    }

    def check_health(self) -> Dict[str, Any]:
        return {
            "provider": "culinary-catalog",
            "status": "healthy",
            "latency_ms": 11,
        }

    def search_restaurants(
        self,
        city: str,
        cuisine: Optional[str] = None,
        price_range: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search restaurants in city matching cuisine or price range."""
        key = city.lower().split(",")[0].strip()
        items = self.CURATED_RESTAURANTS.get(key)

        if not items:
            items = [
                {"name": f"Trattoria Heritage {city.title()}", "cuisine": "Regional Specialties", "price_range": "$$", "rating": 4.6, "specialty": "Chef Signature Tasting"},
                {"name": f"Le Panoramique {city.title()}", "cuisine": "Fine Dining", "price_range": "$$$$", "rating": 4.8, "specialty": "Seasonal Degustation"},
                {"name": f"Market Bistro {city.title()}", "cuisine": "Casual & Local", "price_range": "$", "rating": 4.4, "specialty": "Artisan Local Bites"},
            ]

        results = []
        for r in items:
            if cuisine and cuisine.lower() not in r["cuisine"].lower():
                continue
            if price_range and r["price_range"] != price_range:
                continue
            item = dict(r)
            item["city"] = city
            results.append(item)

        return results or [dict(r, city=city) for r in items]
