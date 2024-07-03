from fastapi import APIRouter, HTTPException
import requests
import logging


from app.schemas import AuthorizationRequest
from app.config import RETURN_BASE, RETURN_ENDPOINT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/request_authorization/")
async def request_authorization(request_body: AuthorizationRequest):

    client_id = request_body.client_id
    redirect_uri = request_body.redirect_uri

    payload = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": ["account-info",
                  "operation-history",
                  "operation-details",
                  "money-source"
                  ]
    }

    response = requests.post("https://yoomoney.ru/oauth/authorize", data=payload)

    logger.info(f"Yoomoney API response: {response.json()}")

    if response.status_code != 302:
        raise HTTPException(status_code=400, detail="Failed to request authorization")

    location = response.headers.get("Location")

    if not location:
        raise HTTPException(status_code=400, detail="No redirection location provided")

    return {"redirect_url": location}
