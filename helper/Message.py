import sys
from config.bankConfig import getBankCode
from datetime import datetime
import random
import json


def getTransactionCode(bizMsgIdr):
    bizMsgIdr = "20001111BBLUIDJA821O0110080002"
    transactionCode = bizMsgIdr[16:19]
    print(transactionCode, file=sys.stderr)
    return transactionCode


def getCreDt():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, file=sys.stderr)
    return f"Timestamp: {timestamp}"


def generateBizMsgIdr(transactionCode):
    formatted_string = "{dateTime}{block}{section}{route}{code}{status}"

    result = formatted_string.format(
        dateTime=datetime.now().strftime('%Y%m%d'),
        block=getBankCode(),
        section="821",
        route="O",
        code="01",
        status=random.randint(000000000, 999999999)
    )

    return str(result)


def generateMsgId(transactionCode):
    formatted_string = "{dateTime}{block}{section}{status}"

    result = formatted_string.format(
        dateTime=datetime.now().strftime('%Y%m%d'),
        block=getBankCode(),
        section="821",
        status=random.randint(000000000, 999999999)
    )

    return str(result)


def replace_placeholders(template, value_dict):
    json_string = json.dumps(template)
    for key, value in value_dict.items():
        placeholder = "{{ " + key + " }}"
        json_string = json_string.replace(placeholder, str(value))
    return json.loads(json_string)


def replace_placeholders_xml(template, value_dict):
    root = ET.fromstring(template)

    for key, value in value_dict.items():
        placeholder = "{" + key + "}"
        for element in root.iter():
            if placeholder in element.text:
                element.text = element.text.replace(placeholder, str(value))

    return ET.tostring(root, encoding='utf-8').decode()
