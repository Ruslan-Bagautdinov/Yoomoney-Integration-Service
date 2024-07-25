import requests
from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

router = APIRouter()


class QuickpayRequest(BaseModel):
    receiver: str
    targets: str
    sum: float
    label: str


class Quickpay:
    def __init__(self, receiver: str, quickpay_form: str, targets: str, paymentType: str, sum: float,
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
    """
    Create a Yoomoney payment.

    Args:
        request_body (QuickpayRequest): The payment request containing the receiver, targets, sum, and label.

    Returns:
        dict: A dictionary containing the redirected URL for the payment.

    Raises:
        HTTPException: If the payment creation fails.
    """
    try:
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
        return {"redirected_url": quickpay.redirected_url}
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
