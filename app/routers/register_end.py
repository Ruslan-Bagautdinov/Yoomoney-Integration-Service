from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from loguru import logger

YM_REDIRECT_URI_BASE = 'https://api.terrapay.online'
YM_REDIRECT_ENDPOINT = '/yoomoney_callback/'

router = APIRouter()


class RegisterEndRequest(BaseModel):
    user_id: str
    client_id: str


class RegisterEndResponse(BaseModel):
    name_for_users: str
    site_address: str
    redirect_uri: str
    notification_uri: str


@router.post("/register_end/")
async def register_end_handler(request_body: RegisterEndRequest):

    logger.info(request_body)

    # найди пользователя в базе по user_id
    # и добавь ему client_id

    response_data = RegisterEndResponse(
        user_id=request_body.user_id,
        client_id=request_body.client_id
    )

    return response_data
