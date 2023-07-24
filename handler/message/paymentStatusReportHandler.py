from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessagePSR(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.028.001.04_PaymentStatusReport.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "000")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "000")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": requestData.get('Fr'),
            "TO_BIC_VALUE": requestData.get('To'),
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
            "CRE_DT_VALUE": handler.getCreDt(),
            "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
            "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "ORGNL_END_TO_END_ID_VALUE": requestData.get('OrgnlEndToEndId'),
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/FIToFIPaymentStatusRequestV04"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
    return response.text


def requestMessageMandateEnquiry(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.017.001.02_MandateEnquiry.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "000")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "000")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": requestData.get('Fr'),
            "TO_BIC_VALUE": requestData.get('To'),
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
            "CRE_DT_VALUE": handler.getCreDt(),
            "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
            "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "MNDTID_VALUE": requestData.get('MndtId'),
            "MNDT_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "TRCKGIND_VALUE": requestData.get('TrckgInd'),
            "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
            "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt') 
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtCpyReq"]["UndrlygCpyReqDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/MandateCopyRequestV02"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
    return response.text