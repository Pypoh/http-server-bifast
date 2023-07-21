from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessageByAccount(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.013.001.08_RequestForPay.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "853")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "853")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": requestData.get('Fr'),
            "TO_BIC_VALUE": requestData.get('To'),
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
            "BIZ_SVC_VALUE": requestData.get('BizSvc'),
            "CRE_DT_VALUE": handler.getCreDt(),
            "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
            "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "NM_OF_TXS_VALUE": requestData.get('NbOfTxs'),
            "INITG_PTY_NM_VALUE": requestData.get('InitgPty_nm'),
            "PSTLADR_CTRY_VALUE": requestData.get('InitgPty_pstladr'),
            "PMTINF_PMTMTD_VALUE": requestData.get('PmtMtd'),
            "PMTTPINF_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "REQD_EXCTN_DT_VALUE": requestData.get('ReqdExctnDt'),
            "XPRY_DT_VALUE": requestData.get('XpryDt'),
            "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_value'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "INSTDAMT_VALUE": requestData.get('InstdAmt_value'),
            "INSTDAMT_CCY_VALUE": requestData.get('InstdAmt_ccy'),
            "CHRGBR_VALUE": requestData.get('ChrgBr'),
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
            "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_value'),
            "CDTR_ACCT_TP_VALUE": requestData.get('CdtrAcct_type'),
            "CDTR_ACCT_NM_VALUE": requestData.get('CdtrAcct_nm'),
            "SPLMNTR_CDTR_TP_VALUE": requestData.get('SplmtryData_Cdtr_tp'),
            "SPLMNTR_CDTR_RSDNTSTS_VALUE": requestData.get('SplmtryData_Cdtr_rsdntsts'),
            "SPLMNTR_CDTR_TWNNM_VALUE": requestData.get('SplmtryData_Cdtr_twnnm'),
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = 853.01
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestV08"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

    return response.text


def requestMessageByProxy(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.013.001.08_RequestForPay.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "851")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "851")

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": requestData.get('Fr'),
            "TO_BIC_VALUE": requestData.get('To'),
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
            "BIZ_SVC_VALUE": requestData.get('BizSvc'),
            "CRE_DT_VALUE": handler.getCreDt(),
            "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
            "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "NM_OF_TXS_VALUE": requestData.get('NbOfTxs'),
            "INITG_PTY_NM_VALUE": requestData.get('InitgPty_nm'),
            "PSTLADR_CTRY_VALUE": requestData.get('InitgPty_pstladr'),
            "PMTINF_PMTMTD_VALUE": requestData.get('PmtMtd'),
            "PMTTPINF_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "REQD_EXCTN_DT_VALUE": requestData.get('ReqdExctnDt'),
            "XPRY_DT_VALUE": requestData.get('XpryDt'),
            "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_value'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "INSTDAMT_VALUE": requestData.get('InstdAmt_value'),
            "INSTDAMT_CCY_VALUE": requestData.get('InstdAmt_ccy'),
            "CHRGBR_VALUE": requestData.get('ChrgBr'),
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
            "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_value'),
            "CDTR_ACCT_TP_VALUE": requestData.get('CdtrAcct_type'),
            "CDTR_ACCT_NM_VALUE": requestData.get('CdtrAcct_nm'),
            "SPLMNTR_CDTR_TP_VALUE": requestData.get('SplmtryData_Cdtr_tp'),
            "SPLMNTR_CDTR_RSDNTSTS_VALUE": requestData.get('SplmtryData_Cdtr_rsdntsts'),
            "SPLMNTR_CDTR_TWNNM_VALUE": requestData.get('SplmtryData_Cdtr_twnnm'),
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    # print(filled_data)

    filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct'].setdefault('Prxy', {})
    filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy'].setdefault('Tp', {})
    filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy']['Tp']['Prtry'] = requestData.get('DbtrAcct_Prxy_tp')
    filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy']['Id'] = requestData.get('DbtrAcct_Prxy_id')
    filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = 851.01
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestV08"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

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
