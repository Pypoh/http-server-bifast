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
    payment_type = paymentData.requestForPaymentByAccount.get('PAYMENT_TYPE')
    dbtr_agt = generalData.sampleData.get('DBTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "END_TO_END_ID_VALUE": generated_biz_msg_idr,
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.requestForPaymentRejectByAccount,
        **paymentData.base,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    return filled_data

def requestMessage(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.014.001.08_RequestForPayReject.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "854")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "854")

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
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "ORGNL_MSG_ID_VALUE": requestData.get('OrgnlMsgId'),
            "ORGNL_MSG_NM_VALUE": requestData.get('OrgnlMsgNmId'),
            "ORGNL_PMTINF_ID_VALUE": requestData.get('OrgnlPmtInfId'),
            "ORGNL_END_TO_END_ID_VALUE": requestData.get('OrgnlEndToEndId'),
            "TXSTS_VALUE": requestData.get('TxSts'),
            "STS_RSN_INF_VALUE": requestData.get('StsRsnInf'),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestStatusReportV08"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
    return response.text


def requestMessageByProxy(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.014.001.08_RequestForPayReject.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "852")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "852")

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
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "ORGNL_MSG_ID_VALUE": requestData.get('OrgnlMsgId'),
            "ORGNL_MSG_NM_VALUE": requestData.get('OrgnlMsgNmId'),
            "ORGNL_PMTINF_ID_VALUE": requestData.get('OrgnlPmtInfId'),
            "ORGNL_END_TO_END_ID_VALUE": requestData.get('OrgnlEndToEndId'),
            "TXSTS_VALUE": requestData.get('TxSts'),
            "STS_RSN_INF_VALUE": requestData.get('StsRsnInf'),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/CreditorPaymentActivationRequestStatusReportV08"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
    return response.text


# def generateResponse(message):
#     filePath = os.path.join(
#         current_app.config["FORMAT_PATH"], 'pacs.002.001.10_AccountEnquiry.json')
#     with open(filePath, 'r') as file:
#         template_data = json.load(file)
#         value_dict = {
#             "FR_BIC_VALUE": BANK_CODE_VALUE,
#             "TO_BIC_VALUE": HUB_CODE_VALUE,
#             "BIZ_MSG_IDR_VALUE": handler.generateBizMsgIdr(
#                 handler.getTagValue(message, "BizMsgIdr")),
#             "CRE_DT_VALUE": handler.getCreDt(),
#             "MSG_ID_VALUE": handler.generateMsgId(bizMsgIdr),
#             "CRE_DT_TM_VALUE": handler.getCreDtTm(),
#             "ORGNL_MSG_ID_VALUE": handler.getTagValue(message, "MsgId"),
#             "ORGNL_MSG_NM_ID_VALUE": handler.getTagValue(message, "MsgDefIdr"),
#             "ORGNL_END_TO_END_ID_VALUE": handler.getTagValue(message, "EndToEndId"),
#             "ORGNL_TX_ID_VALUE": handler.getTagValue(message, "TxId"),
#             "TX_STS_VALUE": "ACTC",
#             "RSN_PRTRY_VALUE": "U000",
#             "ORGNL_CDTR_NM_VALUE": handler.getTagValueNested(
#                 message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/Cdtr/Nm"),
#             "ORGNL_CDTR_ACCT_ID_VALUE": handler.getTagValueNested(
#                 message, "BusMsg/Document/FIToFICstmrCdtTrf/CdtTrfTxInf/CdtrAcct/Id/Othr/Id"),
#             # "ORGNL_CDTR_ACCT_TP_VALUE": handler.getTagValue(message, "CdtrAcct/Id/Othr/Id")
#         }
#     filled_data = handler.replace_placeholders(template_data, value_dict)
#     json_data = json.dumps(filled_data, indent=0)
#     response = Response(json_data, content_type='application/json')
#     return response
