from fastapi import APIRouter, HTTPException, Request
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/issue_invoice", description="Issue an invoice for payment in Yoomoney")
async def issue_invoice(request: Request):
    data = await request.json()
    access_token = data.get("access_token")
    amount = data.get("amount")
    currency = data.get("currency", "RUB")  # Default to Russian Ruble
    label = data.get("label")

    if not access_token:
        raise HTTPException(status_code=400, detail="Access token is required")
    if not amount:
        raise HTTPException(status_code=400, detail="Amount is required")
    if not label:
        raise HTTPException(status_code=400, detail="Label is required")

    url = "https://yoomoney.ru/api/request-payment"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "label": label
    }

    response = requests.post(url, headers=headers, data=payload)

    logger.info(f"Yoomoney API response: {response.json()}")

    if response.status_code == 200:
        payment_details = response.json()
        return payment_details
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to issue invoice")
