from flask import Flask, Response, current_app
import handler.general as handler
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import os
import sys
import requests

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessageByCreditor(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.012.001.06_MandateApproval.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(
        requestData.get('Fr'), "802")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "802")

    timestamp_now = datetime.now()
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_future = timestamp_now + relativedelta(years=1)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": requestData.get('Fr'),
            "TO_BIC_VALUE": requestData.get('Fr'),
            "BIZ_MSG_IDR_VALUE": requestData.get('Fr'),
            "MSG_DEF_IDR_VALUE": requestData.get('Fr'),
            "BIZ_SVC_VALUE": requestData.get('Fr'),
            "CRE_DT_VALUE": requestData.get('Fr'),
            "CPYDPLCT_VALUE": requestData.get('Fr'),
            "PSSBLDPLCT_VALUE": requestData.get('Fr'),
            "MSG_ID_VALUE": requestData.get('Fr'),
            "CRE_DT_TM_VALUE": requestData.get('Fr'),
            "ORGNL_MSG_ID_VALUE": requestData.get('Fr'),
            "ORGNL_MSG_NM_VALUE": requestData.get('Fr'),
            "ACCPTNCRSLT_VALUE": requestData.get('Fr'),
            "ORGNL_MNDT_ID_VALUE": requestData.get('Fr'),
            "ORGNL_MNDT_REQ_ID_VALUE": requestData.get('Fr'),
            "ORGNL_SEQTP_VALUE": requestData.get('Fr'),
            "ORGNL_FR_DT_VALUE": requestData.get('Fr'),
            "ORGNL_TO_DT_VALUE": requestData.get('Fr'),
            "ORGNL_FRST_COLLTN_DT_VALUE": requestData.get('Fr'),
            "ORGNL_FNL_COLLTN_DT_VALUE": requestData.get('Fr'),
            "TRCKGIND_VALUE": requestData.get('Fr'),
            "CDTR_NM_VALUE": requestData.get('Fr'),
            "CDTR_ORG_ID_VALUE": requestData.get('Fr'),
            "CDTR_AGT_VALUE": requestData.get('Fr'),
            "DBTR_NM_VALUE": requestData.get('Fr'),
            "DBTR_AGT_VALUE": requestData.get('Fr'),
            "ORGNL_MNDT_STS_VALUE": requestData.get('Fr')
            }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    # print(filled_data)

    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["FrstColltnAmt"]["value"] = float(
        requestData.get('FrstColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["ColltnAmt"]["value"] = float(
        requestData.get('ColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["MaxAmt"]["value"] = float(
        requestData.get('MaxAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = float(
        requestData.get('Frqcy_cntPerPrd'))
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/MandateInitiationRequestV06"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

    return response.text


def generateResponse(message):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.002.001.10_AccountEnquiry.json')
    bizMsgIdr = handler.generateBizMsgIdr(
        handler.getTagValue(message, "BizMsgIdr"))
    msgId = handler.generateMsgId(bizMsgIdr)
    cdtrNm = handler.getTagValueNested(
        message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/Cdtr/Nm")
    cdtrAcctId = handler.getTagValueNested(
        message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/CdtrAcct/Id/Othr/Id")
    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": bizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": msgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "ORGNL_MSG_ID_VALUE": handler.getTagValue(message, "MsgId"),
            "ORGNL_MSG_NM_ID_VALUE": handler.getTagValue(message, "MsgDefIdr"),
            "ORGNL_END_TO_END_ID_VALUE": handler.getTagValue(message, "EndToEndId"),
            "ORGNL_TX_ID_VALUE": handler.getTagValue(message, "TxId"),
            "TX_STS_VALUE": "ACTC",
            "RSN_PRTRY_VALUE": "U000",
            "ORGNL_CDTR_NM_VALUE": cdtrNm,
            "ORGNL_CDTR_ACCT_ID_VALUE": cdtrAcctId,
            # "ORGNL_CDTR_ACCT_TP_VALUE": handler.getTagValue(message, "CdtrAcct/Id/Othr/Id")
        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    json_data = json.dumps(filled_data, indent=0)
    response = Response(json_data, content_type='application/json')
    return response
