from fastapi import APIRouter, Request, HTTPException, Response
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/yoomoney_callback/{user_id}",
            description="Handle the redirect from Yoomoney after user authorization. "
                        "Exchange the temporary authorization code for an access token.")
async def receive_authorization_code(request: Request, user_id: str):

    logger.info(f"Incoming request: {request.url}")

    code = request.query_params.get("code")
    error = request.query_params.get("error")
    error_description = request.query_params.get("error_description")

    if error:
        raise HTTPException(status_code=400, detail=f"Error: {error}, Description: {error_description}")

    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    #   Здесь тебе надо найти юзера по user_id,
    #   вытащить его client_id, client_secret и redirect_uri
    #   ну и ещё user_redirect_link - куда его послать после оплаты

    client_id = '17EB7B93E988B9716BF4771EB40254425CAFC628C744A0BBDA3B306742BAADE3'
    # client_secret = ''
    redirect_uri = 'https://api.terrapay.online/yoomoney_callback/666'

    if user_id == '666':

        user_redirect_link = 'https://www.youtube.com/watch?v=l2lUfj3wx2Q'

    else:

        user_redirect_link = 'https://www.example.com'

    payload = {
        "code": code,
        "client_id": client_id,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
        # "client_secret": client_secret,
    }

    response = requests.post("https://yoomoney.ru/oauth/token", data=payload)

    logger.info(f"Yoomoney API response: {response.json()}")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange code for access token")

    access_token_response = response.json()
    access_token = access_token_response.get("access_token")

    logger.info(f"access_token: {access_token}")

    #   здесь надо сохранить access_token в базу для юзера
    #   чтобы потом отправлять мне при запросах

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token provided")

    return Response(status_code=302, headers={"Location": user_redirect_link})
