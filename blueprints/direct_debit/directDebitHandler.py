from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessage(mandateForm):
    # Construct file path
    template_filename = 'pacs.003.001.08_DirectDebit.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

    # Generate unique IDs
    payment_type = paymentData.directDebit.get(
        'PAYMENT_TYPE')
    cdtr_agt = generalData.sampleData.get('CDTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(cdtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(cdtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "END_TO_END_ID_VALUE": generated_biz_msg_idr
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.base,
        **paymentData.directDebit,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
        **paymentData.splmtryData,
        **mandateForm,
    }

    # Set the Date
    timestamp_now = datetime.now()
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    value_dict['INTR_BK_STTLM_DT_VALUE'] = timestamp_formatted

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["FIToFICstmrDrctDbt"]["DrctDbtTxInf"][0]["IntrBkSttlmAmt"]["value"] = float(
        value_dict.get('INTR_BK_STTLM_AMT_VALUE'))

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/FIToFICustomerDirectDebitV08"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('CDTR_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)

    return response.text

