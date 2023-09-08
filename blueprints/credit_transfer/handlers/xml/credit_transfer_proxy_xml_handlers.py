from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE

def buildMessage():
    pass

def requestMessage(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pacs.008.001.10_CreditTransferProxy.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(requestData.get('Fr'), "110")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "110")

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
            "STTLMTD_VALUE": requestData.get('SttlmMtd'),
            "END_TO_END_ID_VALUE": generatedBizMsgIdr,
            "TX_ID_VALUE": generatedMsgId,
            "PMT_TP_INF_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "PMT_TP_INF_LCLINSTRM_VALUE": requestData.get('LclInstrm'),
            "INTR_BK_STTLM_AMT_VALUE": requestData.get('IntrBkSttlmAmt_value'),
            "INTR_BK_STTLM_CCY_VALUE": requestData.get('IntrBkSttlmAmt_ccy'),
            "INTR_BK_STTLM_DT_VALUE": handler.getDt(),
            "CHRGBR_VALUE": requestData.get('ChrgBr'),
            "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
            "DBTR_ORG_ID_VALUE": requestData.get('Dbtr_orgid'),
            "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_value'),
            "DBTR_ACCT_TP_VALUE": requestData.get('DbtrAcct_type'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
            "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
            "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_value'),
            "CDTR_ACCT_TP_VALUE": requestData.get('CdtrAcct_type'),
            "CDTR_PRXY_TP_VALUE": requestData.get('CdtrAcct_Prxy_tp'),
            "CDTR_PRXY_ID_VALUE": requestData.get('CdtrAcct_Prxy_id'),
            "RMTINF_USTRD_VALUE": requestData.get('RmtInf'),
            "SPLMNTR_INITACCTID_VALUE": requestData.get('SplmtryData_InitgAcctId'),
            "SPLMNTR_DBTR_TP_VALUE": requestData.get('SplmtryData_Dbtr_tp'),
            "SPLMNTR_DBTR_RSDNTSTS_VALUE": requestData.get('SplmtryData_Dbtr_rsdntsts'),
            "SPLMNTR_DBTR_TWNNM_VALUE": requestData.get('SplmtryData_Dbtr_twnnm'),
            "SPLMNTR_CDTR_TP_VALUE": requestData.get('SplmtryData_Cdtr_tp'),
            "SPLMNTR_CDTR_RSDNTSTS_VALUE": requestData.get('SplmtryData_Cdtr_rsdntsts'),
            "SPLMNTR_CDTR_TWNNM_VALUE": requestData.get('SplmtryData_Cdtr_twnnm'),
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["Document"]["FIToFICstmrCdtTrf"]["CdtTrfTxInf"][0]["IntrBkSttlmAmt"]["value"] = 123.12
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/FIToFICustomerCreditTransferV08"
    }

    response = requests.post(f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
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