import sys
import config.bankConfig as bankConfig
from datetime import datetime
import random
import json
import pytz


def getTagValue(json_data, target_tag):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_tag:
                return value
            elif isinstance(value, (dict, list)):
                result = getTagValue(value, target_tag)
                if result:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = getTagValue(item, target_tag)
            if result:
                return result
    return None


def getTagValueNested(data, target_tag):
    if isinstance(data, dict):
        for key, value in data.items():
            current_tag = key
            if target_tag.startswith(current_tag):
                remaining_tag = target_tag[len(current_tag):].strip("/")
                if remaining_tag:
                    result = getTagValueNested(value, remaining_tag)
                    if result:
                        return result
                else:
                    return value
            elif isinstance(value, (dict, list)):
                result = getTagValueNested(value, target_tag)
                if result:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = getTagValueNested(item, target_tag)
            if result:
                return result
    return None


def printNestedTag(data, parent_key="", indent=""):
    if isinstance(data, dict):
        for key, value in data.items():
            current_key = parent_key + "/" + key if parent_key else key
            # print(indent + current_key)
            if isinstance(value, (dict, list)):
                printNestedTag(value, parent_key=current_key,
                               indent=indent + "  ")


def getTransactionCode(bizMsgIdr):
    # bizMsgIdr = "20001111BBLUIDJA821O0110080002"
    transactionCode = bizMsgIdr[16:19]
    print(transactionCode, file=sys.stderr)
    return transactionCode


def generateBizMsgIdr(bic, bizMsgIdrOrTTC=None):
    formatted_string = "{dateTime}{bankCode}{ttc}{route}{code}{status}"

    result = formatted_string.format(
        dateTime=datetime.now().strftime('%Y%m%d'),
        # bankCode=bankConfig.BANK_CODE_VALUE,
        bankCode=bic,
        ttc=bizMsgIdrOrTTC[16:19] if len(
            bizMsgIdrOrTTC) > 3 else bizMsgIdrOrTTC,
        route="O",
        code="01",
        status=random.randint(10000000, 99999999)
    )

    return result


def generateMsgId(bic, bizMsgIdrOrTTC=None):
    formatted_string = "{dateTime}{bankCode}{ttc}{status}"

    result = formatted_string.format(
        dateTime=datetime.now().strftime('%Y%m%d'),
        bankCode=bic,
        ttc=bizMsgIdrOrTTC[16:19] if len(
            bizMsgIdrOrTTC) > 3 else bizMsgIdrOrTTC,
        status=random.randint(000000000, 999999999)
    )

    return str(result)


def replace_placeholders(template, value_dict):
    json_string = json.dumps(template)
    for key, value in value_dict.items():
        placeholder = "{{ " + key + " }}"
        json_string = json_string.replace(placeholder, str(value))
    return json.loads(json_string)


def getCreDt():
    wibTimeZone = pytz.timezone('Asia/Jakarta')
    currentTime = datetime.now(wibTimeZone)
    creDtValue = currentTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    return creDtValue


def getCreDtTm():
    wibTimeZone = pytz.timezone('Asia/Jakarta')
    currentTime = datetime.now(wibTimeZone)
    creDtTmValue = currentTime.strftime('%Y-%m-%dT%H:%M:%S')
    return creDtTmValue


def getDt():
    wibTimeZone = pytz.timezone('Asia/Jakarta')
    currentTime = datetime.now(wibTimeZone)
    DtValue = currentTime.strftime('%Y-%m-%d')
    return DtValue

def extract_values(json_data):
    def _extract(data, parent_tag=""):
        result_dict = {}
        if isinstance(data, list):
            for i, item in enumerate(data):
                item_tag = parent_tag + str(i)  # Append index to parent_tag
                item_dict = _extract(item, item_tag)
                if item_dict:
                    result_dict.update(item_dict)
        elif isinstance(data, dict):    
            for key, value in data.items():
                if key == "BusMsg": 
                    result_dict.update(_extract(value, parent_tag))
                else:
                    if isinstance(value, (dict, list)):
                        if not parent_tag:
                            result_dict.update(_extract(value, key))
                        else:
                            result_dict.update(_extract(value, f"{parent_tag}_{key}"))
                    else:
                        if not parent_tag:
                            result_dict[key] = value
                        else:
                            result_dict[f"{parent_tag}_{key}"] = value
        return result_dict

    try:
        parsed_data = json.loads(json_data)
        return _extract(parsed_data)
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return None