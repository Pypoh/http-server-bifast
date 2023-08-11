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
        current_app.config["FORMAT_PATH"], 'pain.012.001.06_MandateApproval.json')

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
            "ORGNL_MSG_ID_VALUE": requestData.get('OrgnlMsgInf_msgid'),
            "ORGNL_MSG_NM_VALUE": requestData.get('OrgnlMsgInf_msgnmid'),
            "ACCPTNCRSLT_VALUE": requestData.get('AccptncRslt'),
            "ORGNL_MNDT_ID_VALUE": requestData.get('OrgnlMndt_mndtid'),
            "ORGNL_MNDT_REQ_ID_VALUE": requestData.get('OrgnlMndt_mndtreqid'),
            "ORGNL_SEQTP_VALUE": requestData.get('SeqTp'),
            "ORGNL_FR_DT_VALUE": requestData.get('FrDt'),
            "ORGNL_TO_DT_VALUE": requestData.get('ToDt'),
            "ORGNL_FRST_COLLTN_DT_VALUE": requestData.get('FrstColltnDt'),
            "ORGNL_FNL_COLLTN_DT_VALUE": requestData.get('FnlColltnDt'),
            "TRCKGIND_VALUE": requestData.get('TrckgInd'),
            "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
            "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
            "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
            "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
            "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
            "ORGNL_MNDT_STS_VALUE": requestData.get('OrgnlMndt_sts')
        }

    filled_data = handler.replace_placeholders(template_data, value_dict)

    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["AccptncRslt"]["Accptd"] = True
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/MandateAcceptanceReportV06"
    }

    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

    return response.text


def requestMessage(mandateForm):
    # Construct file path
    template_filename = 'pain.012.001.06_MandateApproval.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

    # Generate unique IDs
    payment_type = paymentData.emandateRegistApprovalByCreditor.get(
        'PAYMENT_TYPE')
    cdtr_agt = generalData.sampleData.get('DBTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(cdtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(cdtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Get data from original mandate
    original_data = {
        "ORGNL_MSG_ID_VALUE": mandateForm.get('ORGNL_MSG_ID_VALUE'),
        "ORGNL_MSG_NM_VALUE": mandateForm.get('ORGNL_MSG_NM_VALUE'),
        "ACCPTNCRSLT_VALUE": mandateForm.get('ACCPTNCRSLT_VALUE'),
        "ORGNL_MNDT_ID_VALUE": mandateForm.get('ORGNL_MNDT_ID_VALUE'),
        "ORGNL_MNDT_REQ_ID_VALUE": mandateForm.get('ORGNL_MNDT_REQ_ID_VALUE'),
        "ORGNL_SEQTP_VALUE": mandateForm.get('ORGNL_SEQTP_VALUE'),
        "ORGNL_FR_DT_VALUE": mandateForm.get('ORGNL_FR_DT_VALUE'),
        "ORGNL_TO_DT_VALUE": mandateForm.get('ORGNL_TO_DT_VALUE'),
        "ORGNL_FRST_COLLTN_DT_VALUE": mandateForm.get('ORGNL_FRST_COLLTN_DT_VALUE'),
        "ORGNL_FNL_COLLTN_DT_VALUE": mandateForm.get('ORGNL_FNL_COLLTN_DT_VALUE'),
        "ORGNL_MNDT_STS_VALUE": mandateForm.get('ORGNL_MNDT_STS_VALUE'),
    }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.base,
        # **original_data,
        **mandateForm,
        **paymentData.emandateRegistApprovalByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["AccptncRslt"]["Accptd"] = True
    
    tags_to_remove = mandateForm.getlist('tags_to_remove')
    # print(f'Tag Found: {tags_to_remove}')

    if tags_to_remove is not None:
        handler.remove_tags(filled_data, tags_to_remove)

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/MandateAcceptanceReportV06"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('DBTR_PORT')}"
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
