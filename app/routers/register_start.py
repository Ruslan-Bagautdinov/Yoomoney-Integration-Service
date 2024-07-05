from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from loguru import logger

YM_REDIRECT_URI_BASE = 'https://api.terrapay.online'
YM_REDIRECT_ENDPOINT = '/yoomoney_callback/'

router = APIRouter()


class RegisterStartRequest(BaseModel):
    user_id: str


class RegisterStartResponse(BaseModel):
    name_for_users: str
    site_address: str
    redirect_uri: str
    notification_uri: str


@router.get("/register_start/")
async def register_start_handler(request_body: RegisterStartRequest):
    logger.info(request_body)

    name_for_users = "TerraPay"
    site_address = YM_REDIRECT_URI_BASE
    redirect_uri = f"{YM_REDIRECT_URI_BASE}{YM_REDIRECT_ENDPOINT}{request_body.user_id}"
    notification_uri = redirect_uri

    response_data = RegisterStartResponse(
        name_for_users=name_for_users,
        site_address=site_address,
        redirect_uri=redirect_uri,
        notification_uri=notification_uri
    )

    return response_data
