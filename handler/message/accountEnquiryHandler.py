from flask import Flask, Response, current_app, jsonify
import requests
import handler.general as handler
from datetime import datetime
import json
import os
import sys

import repository.data as generalData
import repository.payment as paymentData

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessage(requestData):
    # Construct file path
    template_filename = 'pacs.008.001.10_AccountEnquiry.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

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

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.base,
        **paymentData.accountEnquiry,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
        **paymentData.splmtryData
    }

    # with open(filePath, 'r') as file:
    #     template_data = json.load(file)
    #     value_dict = {
    #         "FR_BIC_VALUE": requestData.get('Fr'),
    #         "TO_BIC_VALUE": requestData.get('To') or "FASTIDJA",
    #         "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
    #         "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr') or "pacs.008.001.08",
    #         "CRE_DT_VALUE": handler.getCreDt(),
    #         "MSG_ID_VALUE": generatedMsgId,
    #         "CRE_DT_TM_VALUE": handler.getCreDtTm(),
    #         "NM_OF_TXS_VALUE": requestData.get('NbOfTxs') or "1",
    #         "STTLMTD_VALUE": requestData.get('SttlmMtd') or "CLRG",
    #         "END_TO_END_ID_VALUE": generatedBizMsgIdr,
    #         "TX_ID_VALUE": generatedMsgId,
    #         "PMT_TP_INF_CTGYPURP_VALUE": requestData.get('CtgyPurp') or "51001",
    #         "INTR_BK_STTLM_AMT_VALUE": requestData.get('IntrBkSttlmAmt_value'),
    #         "INTR_BK_STTLM_CCY_VALUE": requestData.get('IntrBkSttlmAmt_ccy') or "IDR",
    #         "CHRGBR_VALUE": requestData.get('ChrgBr') or "DEBT",
    #         "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
    #         "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_value'),
    #         "DBTR_ACCT_TP_VALUE": requestData.get('DbtrAcct_type'),
    #         "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
    #         "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
    #         "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
    #         "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_value'),
    #     }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"][0]["IntrBkSttlmAmt"]["value"] = float(
        value_dict.get('INTR_BK_STTLM_AMT_VALUE'))
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/FIToFICustomerCreditTransferV08"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('HOST_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)

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
