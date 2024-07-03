from pydantic import BaseModel


class AuthorizationRequest(BaseModel):

    client_id: str
    user_id: str
    user_redirect_uri: str
    scope = ["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
    instance_name: str = None


class AuthorizationCodeRequest(BaseModel):
    code: str = None
    error: str = None
    error_description: str = None

