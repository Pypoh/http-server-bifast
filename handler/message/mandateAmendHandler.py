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
        current_app.config["FORMAT_PATH"], 'pain.010.001.06_MandateRegist.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(
        requestData.get('Fr'), "761")
    generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "761")

    timestamp_now = datetime.now()
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_future = timestamp_now + relativedelta(years=1)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')

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
            "AMDMNTRSN_RSN_VALUE": requestData.get('CtgyPurp'),
            "AMDMNTRSN_ADDTLINF_VALUE": requestData.get('CtgyPurp'),
            "MNDT_MNDTID_VALUE": requestData.get('CtgyPurp'),
            "MNDT_REQ_ID_VALUE": generatedBizMsgIdr,
            "MNDT_LCLINSTRM_VALUE": requestData.get('CtgyPurp'), 
            "MNDT_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "OCRNCS_SEQTP_VALUE": requestData.get('SeqTp'),
            "OCRNCS_FRQCY_VALUE": requestData.get('Frqcy_tp'),
            "OCRNCS_CNTPERPRD_VALUE": requestData.get('Frqcy_cntPerPrd'),
            "DRTN_FRDT_VALUE": requestData.get('FrDt') or timestamp_formatted,
            "DRTN_TODT_VALUE": requestData.get('ToDt') or timestamp_future_formatted,
            "FRST_COLLTNDT_VALUE": requestData.get('FrstColltnDt') or timestamp_formatted,
            "FNL_COLLTNDT_VALUE": requestData.get('FnlColltnDt') or timestamp_future_formatted,
            "TRCKGIND_VALUE": requestData.get('TrckgInd'),
            "FRST_COLLTNAMT_CCY_VALUE": requestData.get('FrstColltnAmt_ccy'),
            "FRST_COLLTNAMT_VALUE": requestData.get('FrstColltnAmt_value'),
            "COLLTNAMT_CCY_VALUE": requestData.get('ColltnAmt_ccy'),
            "COLLTNAMT_VALUE": requestData.get('ColltnAmt_value'),
            "MAX_AMT_CCY_VALUE": requestData.get('MaxAmt_ccy'),
            "MAX_AMT_VALUE": requestData.get('MaxAmt_value'),
            "MNDT_RSN_VALUE": requestData.get('Rsn'),
            "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
            "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
            "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_id'),
            "CDTR_ACCT_TP_VALUE": requestData.get('CdtrAcct_tp'),
            "CDTR_ACCT_NM_VALUE": requestData.get('CdtrAcct_nm'),
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
            "DBTR_PRVT_ID_VALUE": requestData.get('Dbtr_prvtid'),
            "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_id'),
            "DBTR_ACCT_TP_VALUE": requestData.get('DbtrAcct_tp'),
            "DBTR_ACCT_NM_VALUE": requestData.get('DbtrAcct_nm'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
            "RFRD_DOC_CDTR_REF_VALUE": requestData.get('CdtrRef'),
            "ORGNLMNDT_MNDTID_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_REQ_ID_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_LCLINSTRM_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_OCRNCS_SEQTP_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_OCRNCS_FRQCY_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DRTN_FRDT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DRTN_TODT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_FRST_COLLTNDT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_FNL_COLLTNDT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_TRCKGIND_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_FRST_COLLTNAMT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_COLLTNAMT_CCY_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_COLLTNAMT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_MAX_AMT_CCY_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_MAX_AMT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_MNDT_RSN_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_NM_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_ORG_ID_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_ACCT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_ACCT_TP_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_ACCT_NM_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_CDTR_AGT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_NM_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_PRVT_ID_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_ACCT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_ACCT_TP_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_ACCT_NM_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_DBTR_AGT_VALUE": requestData.get('CtgyPurp'),
            "ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE": requestData.get('CtgyPurp'),
            "SPLMTRYDATA_ORGNLMNDT_STS": requestData.get('CtgyPurp'),
            "SPLMTRYDATA_MNDT_STS": requestData.get('CtgyPurp')
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

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
        "message": "/MandateAmendmentRequestV06"
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
