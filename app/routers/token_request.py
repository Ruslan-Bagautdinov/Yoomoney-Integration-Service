from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import requests

from main import database
from app.database.models import User
from app.database.schemas import AuthorizationRequest
from app.config import REDIRECT_URI_BASE

router = APIRouter()


@router.post("/request_authorization/")
async def request_authorization(request_body: AuthorizationRequest,
                                session: AsyncSession = Depends(database.get_session)):

    user_id = request_body.user_id
    client_id = request_body.client_id
    user_redirect_uri = request_body.user_redirect_uri

    # Create a new User record in the database
    new_user = User(
        id=user_id,
        access_token=None,
        client_id=client_id,
        user_redirect_uri=user_redirect_uri
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    redirect_uri = f"{REDIRECT_URI_BASE}/receive_authorization_code/{user_id}"

    # Prepare the payload for the POST request
    payload = {
        "client_id": request_body.client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": ["account-info",
                  "operation-history",
                  "operation-details",
                  "incoming-transfers",
                  "payment-p2p",
                  "payment-shop",
                  ]
    }
    if request_body.instance_name:
        payload["instance_name"] = request_body.instance_name

    # Send the POST request to Yoomoney
    response = requests.post("https://yoomoney.ru/oauth/authorize", data=payload)

    # Check if the request was successful
    if response.status_code != 302:
        raise HTTPException(status_code=400, detail="Failed to request authorization")

    # Extract the location header for redirection
    location = response.headers.get("Location")
    if not location:
        raise HTTPException(status_code=400, detail="No redirection location provided")

    # Return the redirection URL
    return {"redirect_url": location}

