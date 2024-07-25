from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

# Own import
from app.config import YM_REDIRECT_URI_BASE, YM_REDIRECT_ENDPOINT


router = APIRouter()


class RegisterEndRequest(BaseModel):
    user_id: str
    client_id: str


class RegisterEndResponse(BaseModel):
    name_for_users: str
    site_address: str
    redirect_uri: str
    notification_uri: str
    client_id: str


@router.post("/register_end/")
async def register_end_handler(request_body: RegisterEndRequest):
    """
    Handle the end of the Yoomoney registration process.

    Args:
        request_body (RegisterEndRequest): The request containing the user ID and client ID.

    Returns:
        RegisterEndResponse: The response containing the registration details.
    """
    try:
        logger.info(request_body)
        # Find the user in the database by user_id and add the client_id to their record

        site_address = f"{YM_REDIRECT_URI_BASE}"
        redirect_uri = f"{YM_REDIRECT_URI_BASE}/{YM_REDIRECT_ENDPOINT}/{request_body.user_id}"
        notification_uri = redirect_uri

        response_data = RegisterEndResponse(
            name_for_users="TerraPay",
            site_address=site_address,
            redirect_uri=redirect_uri,
            notification_uri=notification_uri,
            client_id=request_body.client_id
        )
        return response_data
    except Exception as e:
        logger.error(f"Error in register_end_handler: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
