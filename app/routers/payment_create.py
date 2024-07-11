from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class QuickpayRequest(BaseModel):
    receiver: str
    targets: str
    sum: float
    label: str


class Quickpay:
    def __init__(self,
                 receiver: str,
                 quickpay_form: str,
                 targets: str,
                 paymentType: str,
                 sum: float,
                 label: str = None):
        self.receiver = receiver
        self.quickpay_form = quickpay_form
        self.targets = targets
        self.paymentType = paymentType
        self.sum = sum
        self.label = label

        self.response = self._request()

    def _request(self):
        self.base_url = "https://yoomoney.ru/quickpay/confirm.xml?"

        payload = {
            "receiver": self.receiver,
            "quickpay_form": self.quickpay_form,
            "targets": self.targets,
            "paymentType": self.paymentType,
            "sum": self.sum
        }

        if self.label is not None:
            payload["label"] = self.label

        for key, value in payload.items():
            self.base_url += f"{key.replace('_', '-')}={value}&"

        self.base_url = self.base_url[:-1].replace(" ", "%20")

        response = requests.request("POST", self.base_url)

        self.redirected_url = response.url
        return response


@router.post("/create_payment/")
async def create_payment(request_body: QuickpayRequest):

    quickpay = Quickpay(
        receiver=request_body.receiver,
        quickpay_form="shop",
        targets=request_body.targets,
        paymentType="SB",
        sum=request_body.sum,
        label=request_body.label
    )

    if quickpay.response.status_code != 200:
        raise HTTPException(status_code=quickpay.response.status_code, detail="Failed to create payment")

    # return quickpay.base_url

    return quickpay.redirected_url


#
#
#
# @router.post("/issue_invoice", description="Issue an invoice for payment in Yoomoney")
# async def issue_invoice(request: Request):
#     data = await request.json()
#     access_token = data.get("access_token")
#     amount = data.get("amount")
#     currency = data.get("currency", "RUB")  # Default to Russian Ruble
#     label = data.get("label")
#
#     if not access_token:
#         raise HTTPException(status_code=400, detail="Access token is required")
#     if not amount:
#         raise HTTPException(status_code=400, detail="Amount is required")
#     if not label:
#         raise HTTPException(status_code=400, detail="Label is required")
#
#     url = "https://yoomoney.ru/api/request-payment"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     payload = {
#         "amount": amount,
#         "currency": currency,
#         "label": label
#     }
#
#     response = requests.post(url, headers=headers, data=payload)
#
#     logger.info(f"Yoomoney API response: {response.json()}")
#
#     if response.status_code == 200:
#         payment_details = response.json()
#         return payment_details
#     else:
#         raise HTTPException(status_code=response.status_code, detail="Failed to issue invoice")


