from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime, timedelta

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE

def buildMessage(data):
    # Construct file path
    template_filename = 'pain.014.001.08_RequestForPayReject.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'request_for_payment', 'templates', template_filename)

    # Generate unique IDs
    payment_type = paymentData.requestForPaymentRejectByAccount.get('PAYMENT_TYPE')
    dbtr_agt = generalData.sampleData.get('DBTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "END_TO_END_ID_VALUE": generated_biz_msg_idr,
    }
    
    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": dbtr_agt
    }
    
    ORGNL_END_TO_END_ID_VALUE = data["BusMsg"]["Document"]["FIToFIPmtStsRpt"]["TxInfAndSts"][0]["OrgnlEndToEndId"]
    
    original_data = {
        "ORGNL_MSG_ID_VALUE": generated_msg_id,
        "ORGNL_MSG_NM_VALUE": handler.getMessageNameIdFromTrxCode(ORGNL_END_TO_END_ID_VALUE),
        "ORGNL_PMTINF_ID_VALUE": ORGNL_END_TO_END_ID_VALUE,
        "ORGNL_END_TO_END_ID_VALUE": ORGNL_END_TO_END_ID_VALUE,
        "TXSTS_VALUE": "RJCT",
        "STS_RSN_INF_VALUE": "U110"
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **base_dynamic_data,
        **original_data,
        **paymentData.requestForPaymentRejectByAccount,
        **paymentData.base,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    return filled_data

def requestMessage(message):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(message),
        "message": "/CreditorPaymentActivationRequestStatusReportV08"
    }
    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('DBTR_PORT')}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text
