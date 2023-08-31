import sys
import config.bankConfig as bankConfig
from datetime import datetime
import random
import json
import pytz
import xml.etree.ElementTree as ET
# import repository.payment as paymentData


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
    transactionCode = bizMsgIdr[16:19]
    print(transactionCode, file=sys.stderr)
    return transactionCode


# def getMessageNameIdFromTrxCode(bizMsgIdr):
#     trxCode = getTransactionCode(bizMsgIdr)
#     payment_dictionaries = paymentData.payment_dictionaries
#     for dictionary_name in payment_dictionaries:
#         dictionary = getattr(paymentData, dictionary_name)
#         if dictionary.get("PAYMENT_TYPE") == trxCode:
#             return dictionary.get('MSG_DEF_IDR_VALUE')


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


def bool_to_lower(value):
    return str(value).lower() if isinstance(value, bool) else value


def replace_placeholders_xml(template, value_dict):
    root = ET.fromstring(template)

    for key, value in value_dict.items():
        value = bool_to_lower(value)  # Convert boolean to lowercase string
        placeholder = "{ " + key + " }"
        for element in root.iter():
            if element.text is not None and placeholder in element.text:
                element.text = element.text.replace(placeholder, str(value))

            for attr_name, attr_value in element.attrib.items():
                if placeholder in attr_value:
                    attr_value = attr_value.replace(placeholder, str(value))
                    element.attrib[attr_name] = attr_value

    return ET.tostring(root, encoding='utf-8').decode()


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
                    # Exclude "BusMsg" key from parent_tag
                    result_dict.update(_extract(value, parent_tag))
                else:
                    if isinstance(value, (dict, list)):
                        if not parent_tag:
                            result_dict.update(_extract(value, key))
                        else:
                            result_dict.update(
                                _extract(value, f"{parent_tag}_{key}"))
                    else:
                        if not parent_tag:
                            result_dict[key] = value
                        else:
                            result_dict[f"{parent_tag}_{key}"] = value
        return result_dict

    try:
        parsed_data = json.loads(json_data)
        extracted_data = _extract(parsed_data)
        # Remove the prefix "Document_MndtAccptncRpt_UndrlygAccptncDtls_0_" from the keys
        result_dict1 = {key.replace("Document_MndtAccptncRpt_UndrlygAccptncDtls0_", ""): value for key, value in extracted_data.items()}
        result_dict = {key.replace(
            "OrgnlMndt_", ""): value for key, value in result_dict1.items()}
        return result_dict
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return None


def remove_tags(data, tags_to_remove):
    for tag_path in tags_to_remove:
        keys = tag_path.split('.')
        current_data = data
        for key in keys[:-1]:
            if key.isdigit():
                current_data = current_data[int(key)]  # Handle lists
            else:
                current_data = current_data[key]  # Handle dictionaries
        last_key = keys[-1]
        if isinstance(current_data, list) and last_key.isdigit():
            current_data.pop(int(last_key))  # Remove item from list
        elif last_key in current_data:
            del current_data[last_key]  # Remove key from dictionary
