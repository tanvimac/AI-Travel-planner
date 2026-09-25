from datetime import date
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.trip import Trip
from app.db.models.finance import Budget, Expense
from app.schemas.v1_schemas import BudgetSetRequest, ExpenseCreateRequest
from app.core.errors import NotFoundException

router = APIRouter(prefix="/budget", tags=["Budget & Expenses"])


@router.get("/{trip_id}")
def get_trip_budget(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Get budget summary and expense breakdown for a trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {trip_id} not found", details={"trip_id": trip_id})

    budget = db.query(Budget).filter(Budget.trip_id == trip_id).first()
    expenses = db.query(Expense).filter(Expense.trip_id == trip_id).all()

    total_spent = sum(e.amount for e in expenses)
    spent_by_category: Dict[str, float] = {}
    for e in expenses:
        cat = e.category.lower()
        spent_by_category[cat] = spent_by_category.get(cat, 0.0) + e.amount

    total_allocated = budget.total_budget if budget else trip.budget or 0.0
    remaining = max(0.0, total_allocated - total_spent)

    return {
        "status": "success",
        "trip_id": trip_id,
        "currency": budget.currency if budget else "USD",
        "total_budget": total_allocated,
        "total_spent": round(total_spent, 2),
        "remaining_budget": round(remaining, 2),
        "allocation": {
            "flights": budget.flights_allocated if budget else 0.0,
            "accommodation": budget.accommodation_allocated if budget else 0.0,
            "food": budget.food_allocated if budget else 0.0,
            "activities": budget.activities_allocated if budget else 0.0,
            "transit": budget.transit_allocated if budget else 0.0,
            "misc": budget.misc_allocated if budget else 0.0,
        },
        "spent_by_category": spent_by_category,
        "expense_count": len(expenses),
    }


@router.post("/{trip_id}", status_code=status.HTTP_200_OK)
def set_trip_budget(
    payload: BudgetSetRequest,
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Set or update budget allocation for a trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {trip_id} not found", details={"trip_id": trip_id})

    budget = db.query(Budget).filter(Budget.trip_id == trip_id).first()
    if not budget:
        budget = Budget(
            trip_id=trip_id,
            total_budget=payload.total_budget,
            currency=payload.currency,
            flights_allocated=payload.flights_allocated or 0.0,
            accommodation_allocated=payload.accommodation_allocated or 0.0,
            food_allocated=payload.food_allocated or 0.0,
            activities_allocated=payload.activities_allocated or 0.0,
            transit_allocated=payload.transit_allocated or 0.0,
            misc_allocated=payload.misc_allocated or 0.0,
        )
        db.add(budget)
    else:
        budget.total_budget = payload.total_budget
        budget.currency = payload.currency
        budget.flights_allocated = payload.flights_allocated or 0.0
        budget.accommodation_allocated = payload.accommodation_allocated or 0.0
        budget.food_allocated = payload.food_allocated or 0.0
        budget.activities_allocated = payload.activities_allocated or 0.0
        budget.transit_allocated = payload.transit_allocated or 0.0
        budget.misc_allocated = payload.misc_allocated or 0.0

    # Also update trip overall budget
    trip.budget = payload.total_budget
    db.commit()
    db.refresh(budget)

    return {
        "status": "success",
        "message": "Trip budget updated successfully",
        "budget": {
            "id": budget.id,
            "trip_id": budget.trip_id,
            "total_budget": budget.total_budget,
            "currency": budget.currency,
            "allocations": {
                "flights": budget.flights_allocated,
                "accommodation": budget.accommodation_allocated,
                "food": budget.food_allocated,
                "activities": budget.activities_allocated,
                "transit": budget.transit_allocated,
                "misc": budget.misc_allocated,
            },
        },
    }


@router.get("/{trip_id}/expenses")
def list_trip_expenses(
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """List all recorded expenses for a trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {trip_id} not found", details={"trip_id": trip_id})

    expenses = (
        db.query(Expense)
        .filter(Expense.trip_id == trip_id)
        .order_by(Expense.expense_date.desc(), Expense.id.desc())
        .all()
    )

    return {
        "status": "success",
        "trip_id": trip_id,
        "count": len(expenses),
        "expenses": [
            {
                "id": e.id,
                "category": e.category,
                "amount": e.amount,
                "currency": e.currency,
                "description": e.description,
                "paid_by": e.paid_by,
                "expense_date": e.expense_date.isoformat() if e.expense_date else None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in expenses
        ],
    }


@router.post("/{trip_id}/expenses", status_code=status.HTTP_201_CREATED)
def add_trip_expense(
    payload: ExpenseCreateRequest,
    trip_id: int = Path(..., description="ID of the trip"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Add a new expense item to a trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise NotFoundException(message=f"Trip with ID {trip_id} not found", details={"trip_id": trip_id})

    exp_date = date.today()
    if payload.expense_date:
        try:
            exp_date = date.fromisoformat(payload.expense_date)
        except ValueError:
            pass

    expense = Expense(
        trip_id=trip_id,
        category=payload.category.lower(),
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        paid_by=payload.paid_by or (current_user.full_name if current_user else "Traveler"),
        expense_date=exp_date,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {
        "status": "success",
        "message": "Expense added successfully",
        "expense": {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "currency": expense.currency,
            "description": expense.description,
            "paid_by": expense.paid_by,
            "expense_date": expense.expense_date.isoformat(),
        },
    }


@router.delete("/{trip_id}/expenses/{expense_id}")
def delete_trip_expense(
    trip_id: int = Path(..., description="ID of the trip"),
    expense_id: int = Path(..., description="ID of the expense"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Delete an expense record."""
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.trip_id == trip_id).first()
    if not expense:
        raise NotFoundException(message=f"Expense {expense_id} not found for trip {trip_id}")

    db.delete(expense)
    db.commit()

    return {
        "status": "success",
        "message": f"Expense {expense_id} deleted successfully",
    }
