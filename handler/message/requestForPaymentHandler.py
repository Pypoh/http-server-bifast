from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessageByAccount():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.013.001.08_RequestForPay.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("853")
    generatedMsgId = handler.generateMsgId("853")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "INITG_PTY_NM_VALUE": "Naufal",
            "PSTLADR_CTRY_VALUE": "Postal Address",
            "REQD_EXCTN_DT_VALUE": handler.getDt(),
            "XPRY_DT_VALUE": handler.getDt(),
            # "DBTR_VALUE": ,
            "DBTR_ACCT_VALUE": "12349876",
            "DBTR_AGT_VALUE": "ATOSIDJ1",
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "INSTDAMT_VALUE": 123.12,
            "INSTDAMT_CCY_VALUE": "IDR",
            "CDTR_AGT_VALUE": BANK_CODE_VALUE,
            "CDTR_ORG_ID_VALUE": "PT Abhimata Persada",
            "CDTR_ACCT_VALUE": "98761234",
            "CDTR_ACCT_TP_VALUE": "SVGS",
            "CDTR_ACCT_NM_VALUE": "Naufal Afif",
            "SPLMNTR_CDTR_TP_VALUE": "01",
            "SPLMNTR_CDTR_RSDNTSTS_VALUE": "01",
            "SPLMNTR_CDTR_TWNNM_VALUE": "0300",
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = 123.12

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestV08"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text

def requestMessageByProxy():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.013.001.08_RequestForPay.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("851")
    generatedMsgId = handler.generateMsgId("851")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "INITG_PTY_NM_VALUE": "Naufal",
            "PSTLADR_CTRY_VALUE": "Postal Address",
            "REQD_EXCTN_DT_VALUE": handler.getDt(),
            "XPRY_DT_VALUE": handler.getDt(),
            # "DBTR_VALUE": ,
            "DBTR_ACCT_VALUE": "12349876",
            "DBTR_AGT_VALUE": "ATOSIDJ1",
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "INSTDAMT_VALUE": 123.12,
            "INSTDAMT_CCY_VALUE": "IDR",
            "CDTR_AGT_VALUE": BANK_CODE_VALUE,
            "CDTR_ORG_ID_VALUE": "PT Abhimata Persada",
            "CDTR_ACCT_VALUE": "98761234",
            "CDTR_ACCT_TP_VALUE": "SVGS",
            "CDTR_ACCT_NM_VALUE": "Naufal Afif",
            "SPLMNTR_CDTR_TP_VALUE": "01",
            "SPLMNTR_CDTR_RSDNTSTS_VALUE": "01",
            "SPLMNTR_CDTR_TWNNM_VALUE": "0300",
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = 123.12
    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["DbtrAcct"]["Prxy"]["Tp"]["Prtry"] = "02"
    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["DbtrAcct"]["Prxy"]["Id"] = "naufal.afif@ptap.com"
    
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestV08"
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
