from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessage(id = None):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.028.001.04_PaymentStatusReport.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("000")
    generatedMsgId = handler.generateMsgId("000")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "ORGNL_END_TO_END_ID_VALUE": id,
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/FIToFIPaymentStatusRequestV04"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text


def generateResponse(message):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.002.001.10_AccountEnquiry.json')
    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": handler.generateBizMsgIdr(
                handler.getTagValue(message, "BizMsgIdr")),
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": handler.generateMsgId(bizMsgIdr),
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "ORGNL_MSG_ID_VALUE": handler.getTagValue(message, "MsgId"),
            "ORGNL_MSG_NM_ID_VALUE": handler.getTagValue(message, "MsgDefIdr"),
            "ORGNL_END_TO_END_ID_VALUE": handler.getTagValue(message, "EndToEndId"),
            "ORGNL_TX_ID_VALUE": handler.getTagValue(message, "TxId"),
            "TX_STS_VALUE": "ACTC",
            "RSN_PRTRY_VALUE": "U000",
            "ORGNL_CDTR_NM_VALUE": handler.getTagValueNested(
                message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/Cdtr/Nm"),
            "ORGNL_CDTR_ACCT_ID_VALUE": handler.getTagValueNested(
                message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/CdtrAcct/Id/Othr/Id"),
            # "ORGNL_CDTR_ACCT_TP_VALUE": handler.getTagValue(message, "CdtrAcct/Id/Othr/Id")
        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    json_data = json.dumps(filled_data, indent=0)
    response = Response(json_data, content_type='application/json')
    return response