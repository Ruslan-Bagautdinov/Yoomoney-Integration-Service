from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel
from yoomoney import Client

router = APIRouter()


class PaymentRequest(BaseModel):
    access_token: str
    payment_id: str


@router.post("/check_payment_status/")
async def check_payment_status(request: PaymentRequest):
    """
    Check the status of a Yoomoney payment.

    Args:
        request (PaymentRequest): The payment request containing the access token and payment ID.

    Returns:
        dict: A dictionary containing the payment status details.

    Raises:
        HTTPException: If no operations are found for the given payment ID.
    """
    try:
        client = Client(request.access_token)
        history = client.operation_history(label=request.payment_id)
        if history.operations:
            operation = history.operations[0]
            return {
                "operation_id": operation.operation_id,
                "status": operation.status,
                "datetime": operation.datetime,
                "title": operation.title,
                "direction": operation.direction,
                "amount": operation.amount,
                "label": operation.label
            }
        else:
            raise HTTPException(status_code=404, detail="No operations found for the given payment ID.")
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
