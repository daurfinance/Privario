from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Разрешаем доступ с WebApp (localhost или Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде укажи домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Временная база (словарь вместо БД)
users = {
    "7155546894": {
        "name": "Daurzhan",
        "email": "daurfinance@gmail.com",
        "phone": "+77071234567",
        "card_balance": 500.0,
        "tron_address": "TY1234567890000",
        "tron_balance": 123.45,
        "ton_address": "EQC...abc",
        "ton_balance": 12.3,
        "card_blocked": False
    }
}

class TransferRequest(BaseModel):
    sender_id: str
    to_type: str
    recipient: str
    amount: float

@app.get("/api/user-info")
def get_user_info(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/get-balance")
def get_balance(user_id: str):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "card_balance": user["card_balance"],
        "tron_balance": user["tron_balance"],
        "ton_balance": user["ton_balance"]
    }

@app.post("/api/transfer")
def transfer(req: TransferRequest):
    sender = users.get(req.sender_id)
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    if sender["card_blocked"]:
        raise HTTPException(status_code=403, detail="Card is blocked")

    if sender["card_balance"] < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    sender["card_balance"] -= req.amount
    return {"status": "success", "new_balance": sender["card_balance"]}
