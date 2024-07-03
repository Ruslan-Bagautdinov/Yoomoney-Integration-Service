from fastapi import APIRouter, HTTPException, Request
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/check_invoice_status", description="Check the status of an issued invoice in Yoomoney")
async def check_invoice_status(request: Request):
    data = await request.json()
    access_token = data.get("access_token")
    request_id = data.get("request_id")

    if not access_token:
        raise HTTPException(status_code=400, detail="Access token is required")
    if not request_id:
        raise HTTPException(status_code=400, detail="Request ID is required")

    url = f"https://yoomoney.ru/api/payment/request-status/{request_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers)

    logger.info(f"Yoomoney API response: {response.json()}")

    if response.status_code == 200:
        status_details = response.json()
        return status_details
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to check invoice status")
