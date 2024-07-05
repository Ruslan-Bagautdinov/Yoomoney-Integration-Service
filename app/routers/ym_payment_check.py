import requests
import json
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union
from datetime import datetime

from yoomoney import (
    Account,
    History,
    OperationDetails,
)



from yoomoney.account.balance_details import BalanceDetails
from yoomoney.account.card import Card
from yoomoney.exceptions import InvalidToken

class Account:

    def __init__(self,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,

                 ):

        self.__private_method = method

        self.__private_base_url = base_url
        self.__private_token = token

        data = self._request()

        if len(data) != 0:
            self.account = data['account']
            self.balance = data['balance']
            self.currency = data['currency']
            self.account_status = data['account_status']
            self.account_type = data['account_type']

            self.balance_details = BalanceDetails()
            if 'balance_details' in data:
                if 'available' in data['balance_details']:
                    self.balance_details.available = float(data['balance_details']['available'])
                if 'blocked' in data['balance_details']:
                    self.balance_details.blocked = float(data['balance_details']['blocked'])
                if 'debt' in data['balance_details']:
                    self.balance_details.debt = float(data['balance_details']['debt'])
                if 'deposition_pending' in data['balance_details']:
                    self.balance_details.deposition_pending = float(data['balance_details']['deposition_pending'])
                if 'total' in data['balance_details']:
                    self.balance_details.total = float(data['balance_details']['total'])
                if 'hold' in data['balance_details']:
                    self.balance_details.hold = float(data['balance_details']['hold'])

            self.cards_linked = []
            if 'cards_linked' in data:
                for card_linked in data['cards_linked']:
                    card = Card(pan_fragment=card_linked['pan_fragment'], type=card_linked['type'])
                    self.cards_linked.append(card)
        else:
            raise InvalidToken()

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers)

        return response.json()


from datetime import datetime
from typing import Optional


from yoomoney.operation.operation import Operation

from yoomoney.exceptions import (
    IllegalParamType,
    IllegalParamStartRecord,
    IllegalParamRecords,
    IllegalParamLabel,
    IllegalParamFromDate,
    IllegalParamTillDate,
    TechnicalError
    )


class History:
    def __init__(self,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,
                 type: str = None,
                 label: str = None,
                 from_date: Optional[datetime] = None,
                 till_date: Optional[datetime] = None,
                 start_record: str = None,
                 records: int = None,
                 details: bool = None,
                 ):

        self.__private_method = method

        self.__private_base_url = base_url
        self.__private_token = token

        self.type = type
        self.label = label
        try:
            if from_date is not None:
                from_date = "{Y}-{m}-{d}T{H}:{M}:{S}".format(
                    Y=str(from_date.year),
                    m=str(from_date.month),
                    d=str(from_date.day),
                    H=str(from_date.hour),
                    M=str(from_date.minute),
                    S=str(from_date.second)
                )
        except:
            raise IllegalParamFromDate()

        try:
            if till_date is not None:
                till_date = "{Y}-{m}-{d}T{H}:{M}:{S}".format(
                    Y=str(till_date.year),
                    m=str(till_date.month),
                    d=str(till_date.day),
                    H=str(till_date.hour),
                    M=str(till_date.minute),
                    S=str(till_date.second)
                )
        except:
            IllegalParamTillDate()

        self.from_date = from_date
        self.till_date = till_date
        self.start_record = start_record
        self.records = records
        self.details = details

        data = self._request()

        if "error" in data:
            if data["error"] == "illegal_param_type":
                raise IllegalParamType()
            elif data["error"] == "illegal_param_start_record":
                raise IllegalParamStartRecord()
            elif data["error"] == "illegal_param_records":
                raise IllegalParamRecords()
            elif data["error"] == "illegal_param_label":
                raise IllegalParamLabel()
            elif data["error"] == "illegal_param_from":
                raise IllegalParamFromDate()
            elif data["error"] == "illegal_param_till":
                raise IllegalParamTillDate()
            else:
                raise TechnicalError()


        self.next_record = None
        if "next_record" in data:
            self.next_record = data["next_record"]

        self.operations = list()
        for operation_data in data["operations"]:
            param = {}
            if "operation_id" in operation_data:
                param["operation_id"] = operation_data["operation_id"]
            else:
                param["operation_id"] = None
            if "status" in operation_data:
                param["status"] = operation_data["status"]
            else:
                param["status"] = None
            if "datetime" in operation_data:
                param["datetime"] = datetime.strptime(str(operation_data["datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
            else:
                param["datetime"] = None
            if "title" in operation_data:
                param["title"] = operation_data["title"]
            else:
                param["title"] = None
            if "pattern_id" in operation_data:
                param["pattern_id"] = operation_data["pattern_id"]
            else:
                param["pattern_id"] = None
            if "direction" in operation_data:
                param["direction"] = operation_data["direction"]
            else:
                param["direction"] = None
            if "amount" in operation_data:
                param["amount"] = operation_data["amount"]
            else:
                param["amount"] = None
            if "label" in operation_data:
                param["label"] = operation_data["label"]
            else:
                param["label"] = None
            if "type" in operation_data:
                param["type"] = operation_data["type"]
            else:
                param["type"] = None


            operation = Operation(
                operation_id= param["operation_id"],
                status=param["status"],
                datetime=datetime.strptime(str(param["datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S'),
                title=param["title"],
                pattern_id=param["pattern_id"],
                direction=param["direction"],
                amount=param["amount"],
                label=param["label"],
                type=param["type"],
            )
            self.operations.append(operation)



    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}
        if self.type is not None:
            payload["type"] = self.type
        if self.label is not None:
            payload["label"] = self.label
        if self.from_date is not None:
            payload["from"] = self.from_date
        if self.till_date is not None:
            payload["till"] = self.till_date
        if self.start_record is not None:
            payload["start_record"] = self.start_record
        if self.records is not None:
            payload["records"] = self.records
        if self.details is not None:
            payload["details"] = self.details

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()


from yoomoney.exceptions import (
    IllegalParamOperationId,
    TechnicalError
    )

from yoomoney.operation_details.digital_product import DigitalProduct
from yoomoney.operation_details.digital_bonus import DigitalBonus
from yoomoney.operation_details.digital_good import DigitalGood


class OperationDetails:
    def __init__(self,
                 base_url: str,
                 token: str,
                 operation_id: str,
                 method: str = None,
                 ):
        self.__private_method = method
        self.__private_token = token
        self.__private_base_url = base_url
        self.operation_id = operation_id

        data = self._request()

        if "error" in data:
            if data["error"] == "illegal_param_operation_id":
                raise IllegalParamOperationId()
            else:
                raise TechnicalError()

        self.status = None
        self.pattern_id = None
        self.direction = None
        self.amount = None
        self.amount_due = None
        self.fee = None
        self.datetime = None
        self.title = None
        self.sender = None
        self.recipient = None
        self.recipient_type = None
        self.message = None
        self.comment = None
        self.codepro = None
        self.protection_code = None
        self.expires = None
        self.answer_datetime = None
        self.label = None
        self.details = None
        self.type = None
        self.digital_goods = None

        if "status" in data:
            self.status = data["status"]
        if "pattern_id" in data:
            self.pattern_id = data["pattern_id"]
        if "direction" in data:
            self.direction = data["direction"]
        if "amount" in data:
            self.amount = data["amount"]
        if "amount_due" in data:
            self.amount_due = data["amount_due"]
        if "fee" in data:
            self.fee = data["fee"]
        if "datetime" in data:
            self.datetime = datetime.strptime(str(data["datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "title" in data:
            self.title = data["title"]
        if "sender" in data:
            self.sender = data["sender"]
        if "recipient" in data:
            self.recipient = data["recipient"]
        if "recipient_type" in data:
            self.recipient_type = data["recipient_type"]
        if "message" in data:
            self.message = data["message"]
        if "comment" in data:
            self.comment = data["comment"]
        if "codepro" in data:
            self.codepro = bool(data["codepro"])
        if "protection_code" in data:
            self.protection_code = data["protection_code"]
        if "expires" in data:
            self.datetime = datetime.strptime(str(data["expires"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "answer_datetime" in data:
            self.datetime = datetime.strptime(str(data["answer_datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "label" in data:
            self.label = data["label"]
        if "details" in data:
            self.details = data["details"]
        if "type" in data:
            self.type = data["type"]
        if "digital_goods" in data:
            products: List[DigitalProduct] = []
            for product in data["digital_goods"]["article"]:
                digital_product = DigitalProduct(merchant_article_id=product["merchantArticleId"],
                                                 serial=product["serial"],
                                                 secret=product["secret"],
                                                 )
                products.append(digital_product)

            bonuses: List[DigitalBonus] = []
            for bonus in data["digital_goods"]["bonus"]:
                digital_product = DigitalBonus(serial=bonus["serial"],
                                               secret=bonus["secret"],
                                               )
                bonuses.append(digital_product)

            self.digital_goods = DigitalGood(products=products,
                                             bonuses=bonuses
                                             )

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}

        payload["operation_id"] = self.operation_id


        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()


class Client:
    def __init__(self,
                 token: str = None,
                 base_url: str = None,
                 ):

        if base_url is None:
            self.base_url = "https://yoomoney.ru/api/"

        if token is not None:
            self.token = token



    def account_info(self):
        method = "account-info"
        return Account(base_url=self.base_url,
                       token=self.token,
                       method=method
                       )

    def operation_history(self,
                          type: str = None,
                          label: str = None,
                          from_date: datetime = None,
                          till_date: datetime = None,
                          start_record: str = None,
                          records: int = None,
                          details: bool = None,
                          ):
        method = "operation-history"
        return History(base_url=self.base_url,
                       token=self.token,
                       method=method,
                       type=type,
                       label=label,
                       from_date=from_date,
                       till_date=till_date,
                       start_record=start_record,
                       records=records,
                       details=details,
                       )

    def operation_details(self,
                          operation_id: str
                          ):
        method = "operation-details"
        return OperationDetails(base_url=self.base_url,
                                token=self.token,
                                method=method,
                                operation_id=operation_id,
                                )

from yoomoney import Client
token = "YOUR_TOKEN"
client = Client(token)
history = client.operation_history(label="a1b2c3d4e5")
print("List of operations:")
print("Next page starts with: ", history.next_record)
for operation in history.operations:
    print()
    print("Operation:",operation.operation_id)
    print("\tStatus     -->", operation.status)
    print("\tDatetime   -->", operation.datetime)
    print("\tTitle      -->", operation.title)
    print("\tPattern id -->", operation.pattern_id)
    print("\tDirection  -->", operation.direction)
    print("\tAmount     -->", operation.amount)
    print("\tLabel      -->", operation.label)
    print("\tType       -->", operation.type)



