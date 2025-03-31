# backend/utils.py

import random

def generate_wallet_address():
    return f"TN{random.randint(1000000,9999999)}"

def calculate_commission(amount, type):
    if type == "SWIFT":
        return max(0.02 * amount, 10)
    elif type == "CARD":
        return max(0.03 * amount, 3)
    elif type == "CRYPTO":
        return 3  # + network fee
    elif type == "PRIVARO":
        return 0 if amount <= 10000 else 0.01 * amount
    return 0
