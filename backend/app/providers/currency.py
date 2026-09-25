import logging
from typing import Dict, Any
import requests

logger = logging.getLogger("currency_provider")


class CurrencyProvider:
    """Live foreign exchange currency provider using public rates API."""

    API_URL = "https://api.frankfurter.app/latest"

    # Reference baseline rates against USD (used if external API is down or throttled)
    STATIC_RATES_USD = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 154.5,
        "INR": 86.8,
        "CAD": 1.38,
        "AUD": 1.55,
        "CHF": 0.89,
        "CNY": 7.24,
        "SGD": 1.35,
        "THB": 36.5,
        "AED": 3.67,
    }

    def check_health(self) -> Dict[str, Any]:
        """Verify connectivity to currency provider."""
        try:
            res = requests.get(self.API_URL, params={"from": "USD", "to": "EUR"}, timeout=3)
            return {
                "provider": "frankfurter",
                "status": "healthy" if res.status_code == 200 else "degraded",
                "latency_ms": int(res.elapsed.total_seconds() * 1000),
            }
        except Exception as e:
            logger.warning("Currency provider health check failed: %s", e)
            return {
                "provider": "frankfurter",
                "status": "unhealthy",
                "error": str(e),
            }

    def get_latest_rates(self, base_currency: str = "USD") -> Dict[str, Any]:
        """Fetch real-time exchange rates for a given base currency."""
        base = base_currency.upper()
        try:
            res = requests.get(self.API_URL, params={"from": base}, timeout=4)
            if res.status_code == 200:
                data = res.json()
                rates = data.get("rates", {})
                rates[base] = 1.0
                return {
                    "base": base,
                    "date": data.get("date"),
                    "rates": rates,
                    "source": "live",
                }
        except Exception as exc:
            logger.warning("Failed to fetch live FX rates for %s: %s. Using baseline reference rates.", base, exc)

        # Baseline computation
        base_factor = self.STATIC_RATES_USD.get(base, 1.0)
        computed_rates = {
            curr: round(rate / base_factor, 4)
            for curr, rate in self.STATIC_RATES_USD.items()
        }
        return {
            "base": base,
            "date": "reference",
            "rates": computed_rates,
            "source": "reference_baseline",
        }

    def convert(self, amount: float, from_curr: str, to_curr: str) -> Dict[str, Any]:
        """Convert an amount from one currency to another."""
        from_c = from_curr.upper()
        to_c = to_curr.upper()

        if from_c == to_c:
            return {
                "amount": amount,
                "from_currency": from_c,
                "to_currency": to_c,
                "converted_amount": amount,
                "rate": 1.0,
            }

        rates_data = self.get_latest_rates(from_c)
        rate = rates_data.get("rates", {}).get(to_c)

        if not rate:
            # Fallback cross-rate
            from_usd = self.STATIC_RATES_USD.get(from_c, 1.0)
            to_usd = self.STATIC_RATES_USD.get(to_c, 1.0)
            rate = round(to_usd / from_usd, 4)

        converted = round(amount * rate, 2)
        return {
            "amount": amount,
            "from_currency": from_c,
            "to_currency": to_c,
            "converted_amount": converted,
            "rate": rate,
            "source": rates_data.get("source", "reference_baseline"),
        }
