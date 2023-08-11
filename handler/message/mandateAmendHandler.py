from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessageByCreditor(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'pain.010.001.06_MandateAmend.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr(
        requestData.get('Fr'), requestData.get('Payment_type'))
    generatedMsgId = handler.generateMsgId(
        requestData.get('Fr'), requestData.get('Payment_type'))

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
            "AMDMNTRSN_RSN_VALUE": requestData.get('AmdmntRsn_rsn'),
            "AMDMNTRSN_ADDTLINF_VALUE": requestData.get('AmdmntRsn_addtlInf'),
            "MNDT_MNDTID_VALUE": requestData.get('Mndt_MndtId'),
            "MNDT_REQ_ID_VALUE": generatedBizMsgIdr,
            "MNDT_LCLINSTRM_VALUE": requestData.get('Mndt_LclInstrm'),
            "MNDT_CTGYPURP_VALUE": requestData.get('Mndt_CtgyPurp'),
            "OCRNCS_SEQTP_VALUE": requestData.get('Mndt_SeqTp'),
            "OCRNCS_FRQCY_VALUE": requestData.get('Mndt_Frqcy_tp'),
            "OCRNCS_CNTPERPRD_VALUE": requestData.get('Mndt_Frqcy_cntPerPrd'),
            "DRTN_FRDT_VALUE": requestData.get('Mndt_FrDt') or timestamp_formatted,
            "DRTN_TODT_VALUE": requestData.get('Mndt_ToDt') or timestamp_future_formatted,
            "FRST_COLLTNDT_VALUE": requestData.get('Mndt_FrstColltnDt') or timestamp_formatted,
            "FNL_COLLTNDT_VALUE": requestData.get('Mndt_FnlColltnDt') or timestamp_future_formatted,
            "TRCKGIND_VALUE": requestData.get('Mndt_TrckgInd'),
            "FRST_COLLTNAMT_CCY_VALUE": requestData.get('Mndt_FrstColltnAmt_ccy'),
            "FRST_COLLTNAMT_VALUE": requestData.get('Mndt_FrstColltnAmt_value'),
            "COLLTNAMT_CCY_VALUE": requestData.get('Mndt_ColltnAmt_ccy'),
            "COLLTNAMT_VALUE": requestData.get('Mndt_ColltnAmt_value'),
            "MAX_AMT_CCY_VALUE": requestData.get('Mndt_MaxAmt_ccy'),
            "MAX_AMT_VALUE": requestData.get('Mndt_MaxAmt_value'),
            "MNDT_RSN_VALUE": requestData.get('Mndt_Rsn'),
            "CDTR_NM_VALUE": requestData.get('Mndt_Cdtr_nm'),
            "CDTR_ORG_ID_VALUE": requestData.get('Mndt_Cdtr_orgid'),
            "CDTR_ACCT_VALUE": requestData.get('Mndt_CdtrAcct_id'),
            "CDTR_ACCT_TP_VALUE": requestData.get('Mndt_CdtrAcct_tp'),
            "CDTR_ACCT_NM_VALUE": requestData.get('Mndt_CdtrAcct_nm'),
            "CDTR_AGT_VALUE": requestData.get('Mndt_CdtrAgt'),
            "DBTR_NM_VALUE": requestData.get('Mndt_Dbtr_nm'),
            "DBTR_PRVT_ID_VALUE": requestData.get('Mndt_Dbtr_prvtid'),
            "DBTR_ACCT_VALUE": requestData.get('Mndt_DbtrAcct_id'),
            "DBTR_ACCT_TP_VALUE": requestData.get('Mndt_DbtrAcct_tp'),
            "DBTR_ACCT_NM_VALUE": requestData.get('Mndt_DbtrAcct_nm'),
            "DBTR_AGT_VALUE": requestData.get('Mndt_DbtrAgt'),
            "RFRD_DOC_CDTR_REF_VALUE": requestData.get('Mndt_CdtrRef'),
            "ORGNLMNDT_MNDTID_VALUE": requestData.get('OrgnlMndt_MndtId'),
            "ORGNLMNDT_REQ_ID_VALUE": requestData.get('OrgnlMndt_MndtReqId'),
            "ORGNLMNDT_LCLINSTRM_VALUE": requestData.get('OrgnlMndt_LclInstrm'),
            "ORGNLMNDT_CTGYPURP_VALUE": requestData.get('OrgnlMndt_CtgyPurp'),
            "ORGNLMNDT_OCRNCS_SEQTP_VALUE": requestData.get('OrgnlMndt_SeqTp'),
            "ORGNLMNDT_OCRNCS_FRQCY_VALUE": requestData.get('OrgnlMndt_Frqcy_tp'),
            "ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE": requestData.get('OrgnlMndt_Frqcy_cntPerPrd'),
            "ORGNLMNDT_DRTN_FRDT_VALUE": requestData.get('OrgnlMndt_FrDt'),
            "ORGNLMNDT_DRTN_TODT_VALUE": requestData.get('OrgnlMndt_ToDt'),
            "ORGNLMNDT_FRST_COLLTNDT_VALUE": requestData.get('OrgnlMndt_FrstColltnDt'),
            "ORGNLMNDT_FNL_COLLTNDT_VALUE": requestData.get('OrgnlMndt_FnlColltnDt'),
            "ORGNLMNDT_TRCKGIND_VALUE": requestData.get('OrgnlMndt_TrckgInd'),
            "ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE": requestData.get('OrgnlMndt_FrstColltnAmt_ccy'),
            "ORGNLMNDT_FRST_COLLTNAMT_VALUE": requestData.get('OrgnlMndt_FrstColltnAmt_value'),
            "ORGNLMNDT_COLLTNAMT_CCY_VALUE": requestData.get('OrgnlMndt_ColltnAmt_ccy'),
            "ORGNLMNDT_COLLTNAMT_VALUE": requestData.get('OrgnlMndt_ColltnAmt_value'),
            "ORGNLMNDT_MAX_AMT_CCY_VALUE": requestData.get('OrgnlMndt_MaxAmt_ccy'),
            "ORGNLMNDT_MAX_AMT_VALUE": requestData.get('OrgnlMndt_MaxAmt_value'),
            "ORGNLMNDT_MNDT_RSN_VALUE": requestData.get('OrgnlMndt_Rsn'),
            "ORGNLMNDT_CDTR_NM_VALUE": requestData.get('OrgnlMndt_Cdtr_nm'),
            "ORGNLMNDT_CDTR_ORG_ID_VALUE": requestData.get('OrgnlMndt_Cdtr_orgid'),
            "ORGNLMNDT_CDTR_ACCT_VALUE": requestData.get('OrgnlMndt_CdtrAcct_id'),
            "ORGNLMNDT_CDTR_ACCT_TP_VALUE": requestData.get('OrgnlMndt_CdtrAcct_tp'),
            "ORGNLMNDT_CDTR_ACCT_NM_VALUE": requestData.get('OrgnlMndt_CdtrAcct_nm'),
            "ORGNLMNDT_CDTR_AGT_VALUE": requestData.get('OrgnlMndt_CdtrAgt'),
            "ORGNLMNDT_DBTR_NM_VALUE": requestData.get('OrgnlMndt_Dbtr_nm'),
            "ORGNLMNDT_DBTR_PRVT_ID_VALUE": requestData.get('OrgnlMndt_Dbtr_prvtid'),
            "ORGNLMNDT_DBTR_ACCT_VALUE": requestData.get('OrgnlMndt_DbtrAcct_id'),
            "ORGNLMNDT_DBTR_ACCT_TP_VALUE": requestData.get('OrgnlMndt_DbtrAcct_tp'),
            "ORGNLMNDT_DBTR_ACCT_NM_VALUE": requestData.get('OrgnlMndt_DbtrAcct_nm'),
            "ORGNLMNDT_DBTR_AGT_VALUE": requestData.get('OrgnlMndt_DbtrAgt'),
            "ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE": requestData.get('OrgnlMndt_CdtrRef'),
            "SPLMTRYDATA_ORGNLMNDT_STS": requestData.get('OrgnlMndt_Sts'),
            "SPLMTRYDATA_MNDT_STS": requestData.get('Mndt_Sts')
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        requestData.get('Mndt_Frqcy_cntPerPrd')))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["FrstColltnAmt"]["value"] = float(
        requestData.get('Mndt_FrstColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["ColltnAmt"]["value"] = float(
        requestData.get('Mndt_ColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["MaxAmt"]["value"] = float(
        requestData.get('Mndt_ColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        requestData.get('OrgnlMndt_Frqcy_cntPerPrd')))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["FrstColltnAmt"]["value"] = float(
        requestData.get('OrgnlMndt_FrstColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["ColltnAmt"]["value"] = float(
        requestData.get('OrgnlMndt_ColltnAmt_value'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MaxAmt"]["value"] = float(
        requestData.get('OrgnlMndt_MaxAmt_value'))
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/MandateAmendmentRequestV06"
    }

    # print(filled_data)

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

    return response.text


def requestMessage(mandateForm):
    # Construct file path
    template_filename = 'pain.010.001.06_MandateAmend.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

    # Generate unique IDs
    payment_type = paymentData.emandateAmendmentByCreditor.get('PAYMENT_TYPE')
    cdtr_agt = generalData.sampleData.get('CDTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(cdtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(cdtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "MNDT_REQ_ID_VALUE": generated_biz_msg_idr,
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # original_data = {
    #     "ORGNLMNDT_MNDTID_VALUE": mandateForm.get('ORGNLMNDT_MNDTID_VALUE'),
    #     "ORGNLMNDT_REQ_ID_VALUE": mandateForm.get('ORGNLMNDT_REQ_ID_VALUE'),
    #     "ORGNLMNDT_LCLINSTRM_VALUE": mandateForm.get('ORGNLMNDT_LCLINSTRM_VALUE'),
    #     "ORGNLMNDT_CTGYPURP_VALUE": mandateForm.get('ORGNLMNDT_CTGYPURP_VALUE'),
    #     "ORGNLMNDT_OCRNCS_SEQTP_VALUE": mandateForm.get('ORGNLMNDT_OCRNCS_SEQTP_VALUE'),
    #     "ORGNLMNDT_OCRNCS_FRQCY_VALUE": mandateForm.get('ORGNLMNDT_OCRNCS_FRQCY_VALUE'),
    #     "ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE": mandateForm.get('ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE'),
    #     "ORGNLMNDT_DRTN_FRDT_VALUE": mandateForm.get('ORGNLMNDT_DRTN_FRDT_VALUE'),
    #     "ORGNLMNDT_DRTN_TODT_VALUE": mandateForm.get('ORGNLMNDT_DRTN_TODT_VALUE'),
    #     "ORGNLMNDT_FRST_COLLTNDT_VALUE": mandateForm.get('ORGNLMNDT_FRST_COLLTNDT_VALUE'),
    #     "ORGNLMNDT_FNL_COLLTNDT_VALUE": mandateForm.get('ORGNLMNDT_FNL_COLLTNDT_VALUE'),
    #     "ORGNLMNDT_TRCKGIND_VALUE": mandateForm.get('ORGNLMNDT_TRCKGIND_VALUE'),
    #     "ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE": mandateForm.get('ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE'),
    #     "ORGNLMNDT_FRST_COLLTNAMT_VALUE": mandateForm.get('ORGNLMNDT_FRST_COLLTNAMT_VALUE'),
    #     "ORGNLMNDT_COLLTNAMT_CCY_VALUE": mandateForm.get('ORGNLMNDT_COLLTNAMT_CCY_VALUE'),
    #     "ORGNLMNDT_COLLTNAMT_VALUE": mandateForm.get('ORGNLMNDT_COLLTNAMT_VALUE'),
    #     "ORGNLMNDT_MAX_AMT_CCY_VALUE": mandateForm.get('ORGNLMNDT_MAX_AMT_CCY_VALUE'),
    #     "ORGNLMNDT_MAX_AMT_VALUE": mandateForm.get('ORGNLMNDT_MAX_AMT_VALUE'),
    #     "ORGNLMNDT_MNDT_RSN_VALUE": mandateForm.get('ORGNLMNDT_MNDT_RSN_VALUE'),
    #     "ORGNLMNDT_CDTR_NM_VALUE": mandateForm.get('ORGNLMNDT_CDTR_NM_VALUE'),
    #     "ORGNLMNDT_CDTR_ORG_ID_VALUE": mandateForm.get('ORGNLMNDT_CDTR_ORG_ID_VALUE'),
    #     "ORGNLMNDT_CDTR_ACCT_VALUE": mandateForm.get('ORGNLMNDT_CDTR_ACCT_VALUE'),
    #     "ORGNLMNDT_CDTR_ACCT_TP_VALUE": mandateForm.get('ORGNLMNDT_CDTR_ACCT_TP_VALUE'),
    #     "ORGNLMNDT_CDTR_ACCT_NM_VALUE": mandateForm.get('ORGNLMNDT_CDTR_ACCT_NM_VALUE'),
    #     "ORGNLMNDT_CDTR_AGT_VALUE": mandateForm.get('ORGNLMNDT_CDTR_AGT_VALUE'),
    #     "ORGNLMNDT_DBTR_NM_VALUE": mandateForm.get('ORGNLMNDT_DBTR_NM_VALUE'),
    #     "ORGNLMNDT_DBTR_PRVT_ID_VALUE": mandateForm.get('ORGNLMNDT_DBTR_PRVT_ID_VALUE'),
    #     "ORGNLMNDT_DBTR_ACCT_VALUE": mandateForm.get('ORGNLMNDT_DBTR_ACCT_VALUE'),
    #     "ORGNLMNDT_DBTR_ACCT_TP_VALUE": mandateForm.get('ORGNLMNDT_DBTR_ACCT_TP_VALUE'),
    #     "ORGNLMNDT_DBTR_ACCT_NM_VALUE": mandateForm.get('ORGNLMNDT_DBTR_ACCT_NM_VALUE'),
    #     "ORGNLMNDT_DBTR_AGT_VALUE": mandateForm.get('ORGNLMNDT_DBTR_AGT_VALUE'),
    #     "ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE": mandateForm.get('ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE'),
    # }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **mandateForm,
        **paymentData.base,
        **paymentData.emandateAmendmentByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Set the Date
    timestamp_now = datetime.now()
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_future = timestamp_now + relativedelta(years=1)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    value_dict['DRTN_FRDT_VALUE'] = timestamp_formatted
    value_dict['DRTN_TODT_VALUE'] = timestamp_future_formatted
    value_dict['FRST_COLLTNDT_VALUE'] = timestamp_formatted
    value_dict['FNL_COLLTNDT_VALUE'] = timestamp_future_formatted

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)

    # print(value_dict, file=sys.stderr)

    # Convert payment data
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        value_dict.get('OCRNCS_CNTPERPRD_VALUE')))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["FrstColltnAmt"]["value"] = float(
        value_dict.get('FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["ColltnAmt"]["value"] = float(
        value_dict.get('COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["MaxAmt"]["value"] = float(
        value_dict.get('MAX_AMT_VALUE'))

    # Convert original payment data
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        value_dict.get('ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE')))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["FrstColltnAmt"]["value"] = float(
        value_dict.get('ORGNLMNDT_FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["ColltnAmt"]["value"] = float(
        value_dict.get('ORGNLMNDT_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MaxAmt"]["value"] = float(
        value_dict.get('ORGNLMNDT_MAX_AMT_VALUE'))

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/MandateAmendmentRequestV06"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('CDTR_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)

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
