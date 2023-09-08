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
    # print(data)
    # Construct file path
    template_filename = 'pain.017.001.02_MandateEnquiry.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'mandate', 'templates', template_filename)

    # Generate unique IDs
    payment_type_key = 'PAYMENT_TYPE'
    initiator_dict = {
        'creditor': paymentData.emandateEnquiry,
        'debitor': paymentData.emandateEnquiry
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
    }

    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": agent_value
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    mandate_dict = {}
    nonref = ""

    # Validate if it BizMsgIdr or MndtId
    try:
        # Attempt to parse the date string
        input_string = data.get('SPLMNTR_RLTD_END_TO_END_ID')
        yyyyMMdd = input_string[:8]
        date_object = datetime.strptime(yyyyMMdd, '%Y%m%d')
        mandate_dict = {
            "MNDTID_VALUE": "NONREF",
            "MNDT_CTGYPURP_VALUE": "802"
        }
        nonref = "Y"
        # print(f"{yyyyMMdd} is a valid date.")
    except ValueError:
        mandate_dict = {
            "MNDTID_VALUE": data.get('SPLMNTR_RLTD_END_TO_END_ID'),
            "MNDT_CTGYPURP_VALUE": "802"
        }
        nonref = "N"
        # print(f"{yyyyMMdd} is not a valid date.")

    # # Create mandate data
    # mandate_dict = {
    #     "MNDTID_VALUE": data.get('SPLMNTR_RLTD_END_TO_END_ID'),
    #     # "MNDTID_VALUE": data.get('MNDTID_VALUE'),
    #     "MNDT_CTGYPURP_VALUE": "802"
    # }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **base_dynamic_data,
        **mandate_dict,
        **paymentData.base,
        **paymentData.emandateEnquiry,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }
    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtCpyReq"]["UndrlygCpyReqDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True

    if nonref == "Y":
        filled_data["BusMsg"]["Document"]["MndtCpyReq"]["UndrlygCpyReqDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtReqId"] = data['SPLMNTR_RLTD_END_TO_END_ID']
        

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)


    return filled_data


def requestMessage(message, initiator):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/MandateCopyRequestV02"
    }

    # Get Agent
    agent_key = 'CDTR_PORT' if initiator == 'creditor' else 'DBTR_PORT'
    agent_value = generalData.sampleData.get(agent_key, None)

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{agent_value}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text
