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


# def requestMessagePSR(requestData):
#     filePath = os.path.join(
#         current_app.config["FORMAT_PATH"], 'pacs.028.001.04_PaymentStatusReport.json')

#     generatedBizMsgIdr = handler.generateBizMsgIdr(
#         requestData.get('Fr'), "000")
#     generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "000")

#     with open(filePath, 'r') as file:
#         template_data = json.load(file)
#         value_dict = {
#             "FR_BIC_VALUE": requestData.get('Fr'),
#             "TO_BIC_VALUE": requestData.get('To'),
#             "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
#             "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
#             "CRE_DT_VALUE": handler.getCreDt(),
#             "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
#             "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
#             "MSG_ID_VALUE": generatedMsgId,
#             "CRE_DT_TM_VALUE": handler.getCreDtTm(),
#             "ORGNL_END_TO_END_ID_VALUE": requestData.get('OrgnlEndToEndId'),
#         }

#     filled_data = handler.replace_placeholders(template_data, value_dict)
#     filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

#     headers = {
#         "Content-Type": "application/json",
#         "Content-Length": str(filled_data),
#         "message": "/FIToFIPaymentStatusRequestV04"
#     }

#     response = requests.post(
#         f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
#     return response.text

def requestMessagePSR(transactionForm):
    # Construct file path
    template_filename = 'pacs.028.001.04_PaymentStatusReport.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)
    # Generate unique IDs
    payment_type = paymentData.paymentStatusRequest.get(
        'PAYMENT_TYPE')
    orgn_agt_key = 'DBTRAGT' if transactionForm.get(
        'ORGNAGT') == 'DBTRAGT' else 'CDTRAGT'
    orgn_agt = generalData.sampleData.get(orgn_agt_key)
    generated_biz_msg_idr = handler.generateBizMsgIdr(
        orgn_agt, payment_type)
    generated_msg_id = handler.generateMsgId(orgn_agt, payment_type)
    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "FR_BIC_VALUE": orgn_agt,
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **transactionForm,
        **paymentData.base,
        **paymentData.paymentStatusRequest
    }
    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/FIToFIPaymentStatusRequestV04"
    }
    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('CDTR_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)
    return response.text

# def requestMessageMandateEnquiry(requestData):
#     filePath = os.path.join(
#         current_app.config["FORMAT_PATH"], 'pain.017.001.02_MandateEnquiry.json')

#     generatedBizMsgIdr = handler.generateBizMsgIdr(
#         requestData.get('Fr'), "000")
#     generatedMsgId = handler.generateMsgId(requestData.get('Fr'), "000")

#     with open(filePath, 'r') as file:
#         template_data = json.load(file)
#         value_dict = {
#             "FR_BIC_VALUE": requestData.get('Fr'),
#             "TO_BIC_VALUE": requestData.get('To'),
#             "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
#             "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
#             "BIZ_SVC_VALUE": requestData.get('BizSvc'),
#             "CRE_DT_VALUE": handler.getCreDt(),
#             "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
#             "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
#             "MSG_ID_VALUE": generatedMsgId,
#             "CRE_DT_TM_VALUE": handler.getCreDtTm(),
#             "MNDTID_VALUE": requestData.get('MndtId'),
#             "MNDT_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
#             "TRCKGIND_VALUE": requestData.get('TrckgInd'),
#             "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
#             "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
#             "DBTR_AGT_VALUE": requestData.get('DbtrAgt')
#         }

#     filled_data = handler.replace_placeholders(template_data, value_dict)
#     filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
#     filled_data["BusMsg"]["Document"]["MndtCpyReq"]["UndrlygCpyReqDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True

#     headers = {
#         "Content-Type": "application/json",
#         "Content-Length": str(filled_data),
#         "message": "/MandateCopyRequestV02"
#     }

#     response = requests.post(
#         f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)
#     return response.text


def requestMessageMandateEnquiry(mandateForm):
    # Construct file path
    template_filename = 'pain.017.001.02_MandateEnquiry.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)
    # Generate unique IDs
    payment_type = paymentData.emandateEnquiry.get(
        'PAYMENT_TYPE')
    orgn_agt_key = 'DBTRAGT' if mandateForm.get(
        'ORGNAGT') == 'DBTRAGT' else 'CDTRAGT'
    orgn_agt = generalData.sampleData.get(orgn_agt_key)
    generated_biz_msg_idr = handler.generateBizMsgIdr(
        orgn_agt, payment_type)
    generated_msg_id = handler.generateMsgId(orgn_agt, payment_type)
    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # Create mandate data
    mandate_dict = {
        "FR_BIC_VALUE": orgn_agt,
        "MNDTID_VALUE": mandateForm.get('MNDTID_VALUE'),
        "MNDT_CTGYPURP_VALUE": mandateForm.get('MNDT_CTGYPURP_VALUE')
    }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **mandate_dict,
        **paymentData.base,
        **paymentData.emandateEnquiry,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }
    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtCpyReq"]["UndrlygCpyReqDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/MandateCopyRequestV02"
    }
    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('DBTR_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)
    return response.text
