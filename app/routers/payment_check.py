from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yoomoney import Client

router = APIRouter()


class PaymentRequest(BaseModel):
    access_token: str
    payment_id: str


@router.post("/check_payment_status/")
async def check_payment_status(request: PaymentRequest):

    client = Client(request.access_token)
    history = client.operation_history(label=request.payment_id)
    if history.operations:
        operation = history.operations[0]
        return {
            "operation_id": operation.operation_id,
            "status": operation.status,
            "datetime": operation.datetime,
            "title": operation.title,
            "direction": operation.direction,
            "amount": operation.amount,
            "label": operation.label
        }
    else:
        raise HTTPException(status_code=404, detail="No operations found for the given payment ID.")






















#
#
# # from yoomoney import Client
# token = "4100118214457431.666EC2B3B53A370B86535E72ADDAC813C78743A5A2DFCE18D06A71D1344BC010F007B7F9ED36DB1C65314D19AAE1253B29EBBB3DE5AB18C683BBF14B326E01A33A14455458250BC1254729ED8015936EAEB12391AA241405387F663D34EB1922891AF447E927A656B9C53A07CF2BDEA794AC3A5AD085365933CD3CD1B202DC95"
# client = Client(token)
# history = client.operation_history(label="123test")
# print("List of operations:")
# print("Next page starts with: ", history.next_record)
# for operation in history.operations:
#     print()
#     print("Operation:",operation.operation_id)
#     print("\tStatus     -->", operation.status)
#     print("\tDatetime   -->", operation.datetime)
#     print("\tTitle      -->", operation.title)
#     print("\tPattern id -->", operation.pattern_id)
#     print("\tDirection  -->", operation.direction)
#     print("\tAmount     -->", operation.amount)
#     print("\tLabel      -->", operation.label)
#     print("\tType       -->", operation.type)
#




































# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime
# import requests
#
# router = APIRouter()
#
#
# class PaymentRequest(BaseModel):
#     access_token: str
#     payment_id: str
#
#
# from datetime import datetime as dt
# from typing import Optional
#
# class Operation:
#     def __init__(self,
#                  operation_id: str = None,
#                  status: str = None,
#                  datetime: Optional[dt] = None,
#                  title: str = None,
#                  pattern_id: str = None,
#                  direction: str = None,
#                  amount: float = None,
#                  label: str = None,
#                  type: str = None,
#                  ):
#         self.operation_id = operation_id
#         self.status = status
#         self.datetime = datetime
#         self.title = title
#         self.pattern_id = pattern_id
#         self.direction = direction
#         self.amount = amount
#         self.label = label
#         self.type = type
#
#
# class History:
#     def __init__(self, operations, next_record):
#         self.operations = operations
#         self.next_record = next_record
#
# class Client:
#     def __init__(self, token: str = None, base_url: str = None):
#         if base_url is None:
#             self.base_url = "https://yoomoney.ru/api/"
#         if token is not None:
#             self.token = token
#
#     def operation_history(self, label: str = None):
#         method = "operation-history"
#         url = f"{self.base_url}{method}"
#         headers = {"Authorization": f"Bearer {self.token}"}
#         params = {"label": label} if label else {}
#         response = requests.get(url, headers=headers, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             operations = [Operation(**op) for op in data.get("operations", [])]
#             next_record = data.get("next_record", None)
#             return History(operations, next_record)
#         else:
#             raise HTTPException(status_code=response.status_code, detail=response.text)
#
# @router.post("/check_payment/")
# async def check_payment_status(request: PaymentRequest):
#     client = Client(token=request.access_token)
#     history = client.operation_history(label=request.payment_id)
#     if history.operations:
#         operation = history.operations[0]
#         return {
#             "status": operation.status,
#             "datetime": operation.datetime,
#             "amount": operation.amount
#         }
#     else:
#         raise HTTPException(status_code=404, detail="No operations found for the given payment ID.")
#
#
#
#
#
# # from fastapi import APIRouter, HTTPException, Request
# # import requests
# # import logging
# #
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)
# #
# # router = APIRouter()
# #
# #
# # @router.post("/check_invoice_status", description="Check the status of an issued invoice in Yoomoney")
# # async def check_invoice_status(request: Request):
# #     data = await request.json()
# #     access_token = data.get("access_token")
# #     request_id = data.get("request_id")
# #
# #     if not access_token:
# #         raise HTTPException(status_code=400, detail="Access token is required")
# #     if not request_id:
# #         raise HTTPException(status_code=400, detail="Request ID is required")
# #
# #     url = f"https://yoomoney.ru/api/payment/request-status/{request_id}"
# #     headers = {
# #         "Authorization": f"Bearer {access_token}",
# #         "Content-Type": "application/x-www-form-urlencoded"
# #     }
# #
# #     response = requests.post(url, headers=headers)
# #
# #     logger.info(f"Yoomoney API response: {response.json()}")
# #
# #     if response.status_code == 200:
# #         status_details = response.json()
# #         return status_details
# #     else:
# #         raise HTTPException(status_code=response.status_code, detail="Failed to check invoice status")
