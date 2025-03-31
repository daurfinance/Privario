# backend/routers/auth.py

from fastapi import APIRouter
from backend.utils import generate_wallet_address

router = APIRouter()

@router.post("/register")
def register_user(telegram_id: str, name: str, email: str, phone: str):
    wallet = generate_wallet_address()
    return {
        "status": "success",
        "wallet": wallet,
        "card": {
            "number": "4444 5555 6666 7777",
            "cvc": "123",
            "exp": "12/28",
            "holder": name
        }
    }
