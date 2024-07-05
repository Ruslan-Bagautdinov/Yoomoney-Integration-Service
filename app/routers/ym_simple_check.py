from yoomoney import Client
token = "4100118214457431.666EC2B3B53A370B86535E72ADDAC813C78743A5A2DFCE18D06A71D1344BC010F007B7F9ED36DB1C65314D19AAE1253B29EBBB3DE5AB18C683BBF14B326E01A33A14455458250BC1254729ED8015936EAEB12391AA241405387F663D34EB1922891AF447E927A656B9C53A07CF2BDEA794AC3A5AD085365933CD3CD1B202DC95"
client = Client(token)
history = client.operation_history(label="123test")
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


