from flask import Flask, Response, current_app, jsonify
import requests
import handler.general as handler
from datetime import datetime
import json
import os
import sys

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessage():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.008.001.10_AccountEnquiry.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("510")
    generatedMsgId = handler.generateMsgId("510")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "TX_ID_VALUE": generatedMsgId,
            "INTR_BK_STTLM_AMT_VALUE": 123.12,
            "INTR_BK_STTLM_CCY_VALUE": "IDR",
            "DBTR_NM_VALUE": "PTAP",
            "DBTR_ACCT_VALUE": "Naufal Afif",
            "DBTR_ACCT_TP_VALUE": "SVGS",
            "DBTR_AGT_VALUE": BANK_CODE_VALUE,
            "CDTR_AGT_VALUE": "ATOSIDJ1",
            "CDTR_NM_VALUE": "Afif Naufal",
            "CDTR_ACCT_VALUE": "12341234",
        }
    # jsonResponse = Response(json_data, content_type='application/json')

    filled_data = handler.replace_placeholders(template_data, value_dict)


    # json_data = json.dumps(filled_data, indent=None)
    
    print(filled_data, file=sys.stderr)

    response = requests.post(f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data)

    # if response.status_code == 200:
    #     return 'POST request sent successfully!'
    # else:
    #     return 'Failed to send POST request.'

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
