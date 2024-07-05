from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import logging

from app.config import YM_REDIRECT_URI_BASE, YM_REDIRECT_ENDPOINT

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthorizationRequest(BaseModel):
    user_id: str
    client_id: str


@router.post("/request_authorization/")
async def request_authorization(request_body: AuthorizationRequest):

    scope = ["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop"
             ]

    # scope = ["operation-history", "operation-details", "payment-shop"]

    scope_str = '%20'.join([str(elem) for elem in scope])

    redirect_uri = f"{YM_REDIRECT_URI_BASE}{YM_REDIRECT_ENDPOINT}{request_body.user_id}"

    url = f"https://yoomoney.ru/oauth/authorize?client_id={request_body.client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope_str}"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to request authorization")

    # Check the content type of the response
    if 'application/json' in response.headers.get('Content-Type', ''):
        logger.info(f"Yoomoney API response: {response.json()}")
    else:
        logger.info(f"Yoomoney API response (non-JSON): {response.text}")

    return {"authorization_url": response.url}



# scope=["account-info",
#              "operation-history",
#              "operation-details",
#              "incoming-transfers",
#              # "payment-p2p",
#              # "payment-shop",
#              ]


# from fastapi import APIRouter, HTTPException
# import requests
# import logging
#
# from app.schemas import AuthorizationRequest
#
# router = APIRouter()
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# @router.post("/request_authorization/")
# async def request_authorization(request_body: AuthorizationRequest):
#
#     client_id = request_body.client_id
#     redirect_uri = request_body.redirect_uri
#     scope = ["account-info", "operation-history", "operation-details", "money-source"]
#
#     url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
#           "&redirect_uri={redirect_uri}&scope={scope}".format(client_id=client_id,
#                                                               redirect_uri=redirect_uri,
#                                                               scope='%20'.join([str(elem) for elem in scope]),
#                                                               )
#
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#
#     response = requests.request("POST", url, headers=headers)
#
#     # response = requests.post("https://yoomoney.ru/oauth/authorize", data=payload, headers=headers)
#
#     if response.status_code == 200:
#         return(response.url)
