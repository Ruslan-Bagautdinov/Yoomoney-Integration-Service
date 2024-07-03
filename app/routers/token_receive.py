from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import requests
import uuid

from main import database
from app.database.schemas import AuthorizationCodeRequest
from app.database.models import User
from app.config import CLIENT_ID, REDIRECT_URI_BASE


router = APIRouter()


@router.post("/receive_authorization_code/{user_id}")
async def receive_authorization_code(user_id: str,
                                     authorization_code_request: AuthorizationCodeRequest,
                                     session: AsyncSession = Depends(database.get_session)):
    if authorization_code_request.error:
        raise HTTPException(status_code=400,
                            detail=f"Error: {authorization_code_request.error}, "
                                   f"Description: {authorization_code_request.error_description}")

    # Convert user_id to UUID
    try:
        user_id_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Fetch client_id and user_redirect_uri from the users table
    query = select(User).where(User.id == user_id_uuid)
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    client_id = user.client_id
    user_redirect_uri = user.user_redirect_uri

    if not client_id or not user_redirect_uri:
        raise HTTPException(status_code=400, detail="Client ID or User Redirect URI not found")

    # Construct the redirect URI with the user_id
    redirect_uri = f"{REDIRECT_URI_BASE}/receive_authorization_code/{user_id}"

    data = {
        "code": authorization_code_request.code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response = requests.post("https://yoomoney.ru/oauth/token", data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    access_token = response.json().get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Access token not found in response")

    # Store the access token in the database associated with the user
    user.access_token = access_token
    await session.commit()
    await session.refresh(user)

    # Redirect the user to the user_redirect_uri
    return Response(status_code=302, headers={"Location": user_redirect_uri})

