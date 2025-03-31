# backend/routers/wallet.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/balance")
def get_balance(user_id: str):
    return {"balance": 1200.0}  # mock

@router.post("/deposit")
def deposit(user_id: str, amount: float):
    return {"status": "success", "new_balance": 1200.0 + amount}
