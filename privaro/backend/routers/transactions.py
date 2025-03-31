# backend/routers/transactions.py

from fastapi import APIRouter
from backend.utils import calculate_commission

router = APIRouter()

@router.post("/transfer")
def make_transfer(from_user: str, to_user: str, amount: float, type: str):
    fee = calculate_commission(amount, type)
    total = amount + fee
    return {
        "status": "success",
        "transferred": amount,
        "commission": fee,
        "total": total
    }

@router.get("/history")
def get_history(user_id: str):
    return [
        {"type": "deposit", "amount": 500, "date": "2025-03-30"},
        {"type": "transfer", "amount": -100, "date": "2025-03-31"},
    ]
