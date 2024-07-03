from pydantic import BaseModel
from typing import List


class AuthorizationRequest(BaseModel):

    client_id: str
    user_id: str
    redirect_uri: str   # RETURN_BASE / RETURN_ENDPOINT / user_id


class AuthorizationCodeRequest(BaseModel):
    code: str = None
    error: str = None
    error_description: str = None
