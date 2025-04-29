# payment_router.py
from fastapi import APIRouter, Request

router = APIRouter()

# Webhook or callback for Stripe/PayFast success
@router.post("/webhook/payment")
async def handle_payment_notification(request: Request):
    data = await request.json()
    # TODO: validate Stripe or PayFast signature if required

    # Example flagging logic (mock)
    business = data.get("business_name")
    email = data.get("email")
    amount = data.get("amount")

    print(f"[INFO] Payment received from {email} for R{amount} - {business}")
    # Flag CRM record for deposit received

    return {"message": "Payment recorded"}
