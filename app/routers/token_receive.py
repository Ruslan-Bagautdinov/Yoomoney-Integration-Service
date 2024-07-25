import requests
from fastapi import APIRouter, Request, HTTPException
from loguru import logger

router = APIRouter()

error_messages = {
    "invalid_request": "Required query parameters are missing or have incorrect or invalid values",
    "unauthorized_client": "Invalid parameter value 'client_id' or 'client_secret', or the application does not have the right to request authorization (for example, YooMoney blocked it 'client_id')",
    "invalid_grant": "In issue 'access_token' denied. YooMoney did not issue a temporary token, the token is expired, or this temporary token has already been issued 'access_token' (repeated request for an authorization token with the same temporary token)",
    "empty_token": "Response token is empty. Repeated request for an authorization token"
}


@router.get("/yoomoney_callback/{user_id}")
async def yoomoney_callback(request: Request, user_id: str):
    """
    Handle the Yoomoney callback to receive the authorization code and exchange it for an access token.

    Args:
        request (Request): The incoming request containing the authorization code.
        user_id (str): The user ID.

    Returns:
        dict: A dictionary containing the access token.

    Raises:
        HTTPException: If the code parameter is missing or if there is an error in the token exchange process.
    """
    try:
        logger.info(f"Received request for user {user_id}")
        logger.info(request)
        query_params = request.query_params
        code = query_params.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Code parameter is missing")
        client_id = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        redirect_uri = "https://example.com/yoomoney_callback/12345"
        url = f"https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&grant_type=authorization_code&redirect_uri={redirect_uri}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, headers=headers)
        logger.info(f"Received response for user {user_id}")
        logger.info(response)
        if "error" in response.json():
            logger.error(response.json())
            error = response.json()["error"]
            error_detail = error_messages.get(error, "Unknown error")
            return {"error": error_detail}
        if response.json()['access_token'] == "":
            logger.error(response.json())
            return {"error": error_messages["empty_token"]}
        access_token = response.json()['access_token']
        logger.info(f"access_token: {access_token}")
        # Save the access_token
        return {"access_token": access_token}
    except Exception as e:
        logger.error(f"Error in yoomoney_callback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
