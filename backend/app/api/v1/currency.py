from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.db.models.finance import CurrencyRate
from app.schemas.v1_schemas import CurrencyConvertRequest
from app.providers.currency import CurrencyProvider

router = APIRouter(prefix="/currency", tags=["Currency & FX"])
provider = CurrencyProvider()


@router.get("/rates")
def get_exchange_rates(
    base: str = Query(default="USD", min_length=3, max_length=4),
    db: Session = Depends(get_db),
):
    """Fetch live or central bank reference foreign exchange rates."""
    data = provider.get_latest_rates(base_currency=base)

    # Cache target rates in database
    base_cur = data.get("base", "USD")
    rates = data.get("rates", {})
    for target_cur, rate in list(rates.items())[:10]:
        rate_entry = CurrencyRate(
            base_currency=base_cur,
            target_currency=target_cur,
            rate=float(rate),
            updated_date=date.today(),
        )
        try:
            db.add(rate_entry)
            db.commit()
        except Exception:
            db.rollback()

    return data


@router.post("/convert")
def convert_currency(request: CurrencyConvertRequest):
    """Convert an amount from one fiat currency to another."""
    return provider.convert(
        amount=request.amount,
        from_curr=request.from_currency,
        to_curr=request.to_currency,
    )
