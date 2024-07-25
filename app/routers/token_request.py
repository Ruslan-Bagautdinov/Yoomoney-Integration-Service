import requests
from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

# Own import
from app.config import YM_REDIRECT_URI_BASE, YM_REDIRECT_ENDPOINT

router = APIRouter()

logger.add("app.log", rotation="500 MB")


class AuthorizationRequest(BaseModel):
    user_id: str
    client_id: str


@router.post("/request_authorization/")
async def request_authorization(request_body: AuthorizationRequest):
    """
    Request authorization from Yoomoney.

    Args:
        request_body (AuthorizationRequest): The request containing the user ID and client ID.

    Returns:
        dict: A dictionary containing the authorization URL.

    Raises:
        HTTPException: If the authorization request fails.
    """
    try:
        scope = ["account-info", "operation-history", "operation-details", "incoming-transfers", "payment-p2p",
                 "payment-shop"]
        scope_str = '%20'.join([str(elem) for elem in scope])
        redirect_uri = f"{YM_REDIRECT_URI_BASE}{YM_REDIRECT_ENDPOINT}{request_body.user_id}"
        url = f"https://yoomoney.ru/oauth/authorize?client_id={request_body.client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope_str}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to request authorization")
        if 'application/json' in response.headers.get('Content-Type', ''):
            logger.info(f"Yoomoney API response: {response.json()}")
        else:
            logger.info(f"Yoomoney API response (non-JSON): {response.text}")
        return {"authorization_url": response.url}
    except Exception as e:
        logger.error(f"Error in request_authorization: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
