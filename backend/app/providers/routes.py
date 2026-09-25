import hashlib
from typing import Dict, Any, List


class RouteProvider:
    """Transit, driving, and multimodal navigation route provider."""

    def check_health(self) -> Dict[str, Any]:
        return {
            "provider": "transit-router",
            "status": "healthy",
            "latency_ms": 14,
        }

    def plan_route(
        self,
        origin: str,
        destination: str,
        mode: str = "transit",
    ) -> Dict[str, Any]:
        """Compute navigation steps, distance, and duration between points."""
        seed_key = f"{origin.lower()}-{destination.lower()}-{mode.lower()}"
        seed = int(hashlib.md5(seed_key.encode()).hexdigest()[:6], 16)

        mode_clean = mode.lower()
        if mode_clean == "walking":
            speed_kmh = 4.5
            cost = 0.0
            dist_km = round(1.5 + (seed % 6), 1)
        elif mode_clean == "driving":
            speed_kmh = 38.0
            cost = round(12.0 + (seed % 35), 2)
            dist_km = round(5.0 + (seed % 45), 1)
        elif mode_clean == "flight":
            speed_kmh = 650.0
            cost = round(120.0 + (seed % 350), 2)
            dist_km = round(250.0 + (seed % 1200), 1)
        else: # transit
            speed_kmh = 28.0
            cost = round(3.5 + (seed % 15), 2)
            dist_km = round(3.0 + (seed % 25), 1)

        duration_mins = max(int((dist_km / speed_kmh) * 60), 5)

        steps: List[str] = [
            f"Depart from {origin}",
            f"Take {mode_clean} toward central corridor (approx. {dist_km * 0.6:.1f} km)",
            f"Transfer/continue toward destination sector ({dist_km * 0.4:.1f} km)",
            f"Arrive at {destination}",
        ]

        return {
            "origin": origin,
            "destination": destination,
            "transport_mode": mode_clean,
            "distance_km": dist_km,
            "duration_minutes": duration_mins,
            "estimated_cost": cost,
            "currency": "USD",
            "steps": steps,
        }


RoutesProvider = RouteProvider

