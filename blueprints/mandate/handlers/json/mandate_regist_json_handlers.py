from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import socket
import xml.etree.ElementTree as ET
import struct
import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def buildMessage(data, initiator):
    # Construct file path
    # template_filename = 'pain.009.001.06_MandateRegist_wo_colamt.json'
    template_filename = 'pain.009.001.06_MandateRegist.json'
    # template_filename = 'pain.009.001.06_MandateRegist_wo_cntperprd.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'mandate', 'templates', template_filename)

    # Generate unique IDs
    payment_type_key = 'PAYMENT_TYPE'
    initiator_dict = {
        'creditor': paymentData.emandateRegistrationByCreditor,
        'debitor': paymentData.emandateRegistrationByDebitor
    }
    payment_type = initiator_dict.get(initiator, {}).get(payment_type_key)
    agent_key = 'CDTRAGT' if initiator == 'creditor' else 'DBTRAGT'
    agent_value = generalData.sampleData.get(agent_key, None)

    generated_biz_msg_idr = handler.generateBizMsgIdr(
        agent_value, payment_type)
    generated_msg_id = handler.generateMsgId(agent_value, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "MNDT_REQ_ID_VALUE": generated_biz_msg_idr,
    }

    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": agent_value
    }

    payment_dynamic_data = {
        # "INTR_BK_STTLM_DT_VALUE": handler.getCreDt(),
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **base_dynamic_data,
        **payment_dynamic_data,
        **paymentData.base,
        **paymentData.emandateRegistrationByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Set the Date
    timestamp_now = datetime.now()
    # timestamp_now = datetime.now() - timedelta(days=7)
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_first = datetime.now()
    # timestamp_first = datetime.now() + timedelta(days=1)
    timestamp_first_formatted = timestamp_first.strftime('%Y-%m-%d')
    # timestamp_future = datetime.now() - timedelta(days=2)
    timestamp_future = timestamp_now + relativedelta(years=1)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    value_dict['DRTN_FRDT_VALUE'] = timestamp_formatted
    value_dict['DRTN_TODT_VALUE'] = timestamp_future_formatted
    value_dict['FRST_COLLTNDT_VALUE'] = timestamp_first_formatted
    value_dict['FNL_COLLTNDT_VALUE'] = timestamp_future_formatted

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["FrstColltnAmt"]["value"] = float(
        value_dict.get('FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["ColltnAmt"]["value"] = float(
        value_dict.get('COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["MaxAmt"]["value"] = float(
        value_dict.get('MAX_AMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = float(
        value_dict.get('OCRNCS_CNTPERPRD_VALUE'))

    # print(data)
    tags_to_remove = data.get('TAGS_TO_REMOVE_REGIST')
    # print(f'Tag Found: {tags_to_remove}')

    if tags_to_remove is not None:
        handler.remove_tags(filled_data, tags_to_remove)

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)
    return filled_data


def requestMessage(message, initiator):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/MandateInitiationRequestV06"
    }

    # Get Agent
    agent_key = 'CDTR_PORT' if initiator == 'creditor' else 'DBTR_PORT'
    agent_value = generalData.sampleData.get(agent_key, None)

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{agent_value}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text
