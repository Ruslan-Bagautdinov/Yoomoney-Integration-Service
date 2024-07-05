from fastapi import APIRouter, Request, HTTPException, Response
import requests
from loguru import logger

router = APIRouter()

error_messages = {
    "invalid_request": "Required query parameters are missing or have incorrect or invalid values",
    "unauthorized_client": "Invalid parameter value 'client_id' or 'client_secret', "
                           "or the application does not have the right to request authorization (for example, "
                           "YooMoney blocked it 'client_id')",
    "invalid_grant": "In issue 'access_token' denied. YooMoney did not issue a temporary token, "
                     "the token is expired, or this temporary token has already been issued 'access_token' "
                     "(repeated request for an authorization token with the same temporary token)",
    "empty_token": "Response token is empty. Repeated request for an authorization token"
}


@router.get("/yoomoney_callback/{user_id}")
async def yoomoney_callback(request: Request, user_id: str):

    logger.info(f"Received request for user {user_id}")
    logger.info(request)

    query_params = request.query_params
    code = query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Code parameter is missing")

    #   здесь тебе надо найти юзера по user_id,
    #   вытащить его client_id и redirect_uri  (которые были указан при регистрации)

    client_id = "97B58162A924D88E1CF062BA57F8081BFE4F80343361E2CC459537A44D28D838"
    redirect_uri = "https://api.terrapay.online/yoomoney_callback/777"

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

    # здесь надо сохранить access_token

    return {"access_token": access_token}


#
# @router.get("/yoomoney_callback/{user_id}",
#             description="Handle the redirect from Yoomoney after user authorization. "
#                         "Exchange the temporary authorization code for an access token.")
# async def receive_authorization_code(request: Request, user_id: str):
#
#     logger.info(f"Incoming request: {request.url}")
#
#     code = request.query_params.get("code")
#     error = request.query_params.get("error")
#     error_description = request.query_params.get("error_description")
#
#     if error:
#         raise HTTPException(status_code=400, detail=f"Error: {error}, Description: {error_description}")
#
#     if not code:
#         raise HTTPException(status_code=400, detail="No code provided")
#
#     #   Здесь тебе надо найти юзера по user_id,
#     #   вытащить его client_id, client_secret и redirect_uri
#     #   ну и ещё user_redirect_link - куда его послать после оплаты
#
#     client_id = '17EB7B93E988B9716BF4771EB40254425CAFC628C744A0BBDA3B306742BAADE3'
#     # client_secret = ''
#     redirect_uri = 'https://api.terrapay.online/yoomoney_callback/666'
#
#     if user_id == '666':
#
#         user_redirect_link = 'https://www.youtube.com/watch?v=l2lUfj3wx2Q'
#
#     else:
#
#         user_redirect_link = 'https://www.example.com'
#
#     payload = {
#         "code": code,
#         "client_id": client_id,
#         "grant_type": "authorization_code",
#         "redirect_uri": redirect_uri
#         # "client_secret": client_secret,
#     }
#
#     response = requests.post("https://yoomoney.ru/oauth/token", data=payload)
#
#     logger.info(f"Yoomoney API response: {response.json()}")
#
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Failed to exchange code for access token")
#
#     access_token_response = response.json()
#     access_token = access_token_response.get("access_token")
#
#     logger.info(f"access_token: {access_token}")
#
#     #   здесь надо сохранить access_token в базу для юзера
#     #   чтобы потом отправлять мне при запросах
#
#     if not access_token:
#         raise HTTPException(status_code=400, detail="No access token provided")
#
#     return Response(status_code=302, headers={"Location": user_redirect_link})
