from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

# Own import
from app.config import YM_REDIRECT_URI_BASE, YM_REDIRECT_ENDPOINT


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
    """
    Handle the start of the Yoomoney registration process.

    Args:
        request_body (RegisterStartRequest): The request containing the user ID.

    Returns:
        RegisterStartResponse: The response containing the registration details.
    """
    try:
        logger.info(request_body)
        name_for_users = "YourSystemName"
        site_address = f"{YM_REDIRECT_URI_BASE}"
        redirect_uri = f"{YM_REDIRECT_URI_BASE}/{YM_REDIRECT_ENDPOINT}/{request_body.user_id}"
        notification_uri = redirect_uri

        response_data = RegisterStartResponse(
            name_for_users=name_for_users,
            site_address=site_address,
            redirect_uri=redirect_uri,
            notification_uri=notification_uri
        )
        return response_data
    except Exception as e:
        logger.error(f"Error in register_start_handler: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
