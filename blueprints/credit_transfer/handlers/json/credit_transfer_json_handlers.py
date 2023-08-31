from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE

def buildMessage(data):
    # Construct file path
    template_filename = 'pacs.008.001.10_CreditTransfer.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'credit_transfer','templates', template_filename)
    # Generate unique IDs
    payment_type = paymentData.creditTransfer.get('PAYMENT_TYPE')
    dbtr_agt = generalData.sampleData.get('DBTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "END_TO_END_ID_VALUE": generated_biz_msg_idr,
        "TX_ID_VALUE": generated_msg_id,
    }
    
    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": dbtr_agt
    }
    
    payment_dynamic_data = {
        "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
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
        **paymentData.creditTransfer,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
        **paymentData.splmtryData
    }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"][0]["IntrBkSttlmAmt"]["value"] = float(
        value_dict.get('INTR_BK_STTLM_AMT_VALUE'))
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    return filled_data

def requestMessage(message):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/FIToFICustomerCreditTransferV08"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('DBTR_PORT')}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text