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


def buildMessage(data, initiator):
    # Construct file path
    template_filename = 'pain.012.001.06_MandateApproval.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'mandate', 'templates', template_filename)

    # Validate Ids
    input_data = data.get('INPUT_DATA')
    related_data = data.get('RELATED_DATA')
    mandate_data = input_data if related_data is None else related_data
    ORGNL_MNDT_REQ_ID_VALUE = ""
    indicator_dict = {}
    try:
        yyyyMMdd = mandate_data[:8]
        date_object = datetime.strptime(yyyyMMdd, '%Y%m%d')
        ORGNL_MNDT_REQ_ID_VALUE = mandate_data
    except ValueError:
        ORGNL_MNDT_REQ_ID_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"][
            "UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtReqId"]

    trx_code = ORGNL_MNDT_REQ_ID_VALUE[16:20]
    if (trx_code[0] == "8"):
        initiator_dict = {
            'creditor': paymentData.emandateRegistApprovalByCreditor,
            'debitor': paymentData.emandateRegistApprovalByDebitor
        }
    else:
        initiator_dict = {
            'creditor': paymentData.emandateAmendApprovalByCreditor,
            'debitor': paymentData.emandateAmendApprovalByDebitor
        }
    payment_type_key = 'PAYMENT_TYPE'
    # initiator_dict = {
    #     'creditor': paymentData.emandateRegistApprovalByCreditor,
    #     'debitor': paymentData.emandateRegistApprovalByCreditor
    # }
    payment_type = initiator_dict.get(initiator, {}).get(payment_type_key)
    agent_key = 'DBTRAGT' if initiator == 'creditor' else 'CDTRAGT'
    agent_value = generalData.sampleData.get(agent_key, None)
    generated_biz_msg_idr = handler.generateBizMsgIdr(
        agent_value, payment_type)
    generated_msg_id = handler.generateMsgId(agent_value, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
    }

    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": agent_value
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    # ORGNL_MNDT_REQ_ID_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"][
    #     "UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtReqId"]

    ORGNL_MSG_NM_VALUE = handler.getMessageNameIdFromTrxCode(ORGNL_MNDT_REQ_ID_VALUE)

    original_data = {
        "ORGNL_MSG_ID_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["GrpHdr"]["MsgId"],
        "ORGNL_MSG_NM_VALUE": ORGNL_MSG_NM_VALUE,
        "ACCPTNCRSLT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"],
        "ORGNL_MNDT_ID_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtId"],
        "ORGNL_MNDT_REQ_ID_VALUE": ORGNL_MNDT_REQ_ID_VALUE,
        "ORGNL_SEQTP_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["SeqTp"],
        "ORGNL_FR_DT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["FrDt"],
        "ORGNL_TO_DT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["ToDt"],
        "ORGNL_FRST_COLLTN_DT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FrstColltnDt"],
        "ORGNL_FNL_COLLTN_DT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FrstColltnDt"],
        "ORGNL_MNDT_STS_VALUE": "ACTV",
    }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.base,
        **original_data,
        **base_dynamic_data,
        **paymentData.emandateRegistApprovalByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["AccptncRslt"]["Accptd"] = True

    # tags_to_remove = data.getlist('tags_to_remove')
    # # print(f'Tag Found: {tags_to_remove}')

    # if tags_to_remove is not None:
    #     handler.remove_tags(filled_data, tags_to_remove)

    # Print filled data (for debugging)
    # print(filled_data, file  =sys.stderr)

    return filled_data


def requestMessage(message, initiator):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/MandateAcceptanceReportV06"
    }

    # Get Agent
    agent_key = 'DBTR_PORT' if initiator == 'creditor' else 'CDTR_PORT'
    agent_value = generalData.sampleData.get(agent_key, None)

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{agent_value}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text

# def requestMessageByCreditor(requestData):
#     filePath = os.path.join(
#         current_app.config["FORMAT_PATH"], 'pain.012.001.06_MandateApproval.json')

#     generatedBizMsgIdr = handler.generateBizMsgIdr(
#         requestData.get('Fr'), requestData.get('Payment_type'))
#     generatedMsgId = handler.generateMsgId(
#         requestData.get('Fr'), requestData.get('Payment_type'))

#     timestamp_now = datetime.now()
#     timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
#     timestamp_future = timestamp_now + relativedelta(years=1)
#     timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')

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
#             "ORGNL_MSG_ID_VALUE": requestData.get('OrgnlMsgInf_msgid'),
#             "ORGNL_MSG_NM_VALUE": requestData.get('OrgnlMsgInf_msgnmid'),
#             "ACCPTNCRSLT_VALUE": requestData.get('AccptncRslt'),
#             "ORGNL_MNDT_ID_VALUE": requestData.get('OrgnlMndt_mndtid'),
#             "ORGNL_MNDT_REQ_ID_VALUE": requestData.get('OrgnlMndt_mndtreqid'),
#             "ORGNL_SEQTP_VALUE": requestData.get('SeqTp'),
#             "ORGNL_FR_DT_VALUE": requestData.get('FrDt'),
#             "ORGNL_TO_DT_VALUE": requestData.get('ToDt'),
#             "ORGNL_FRST_COLLTN_DT_VALUE": requestData.get('FrstColltnDt'),
#             "ORGNL_FNL_COLLTN_DT_VALUE": requestData.get('FnlColltnDt'),
#             "TRCKGIND_VALUE": requestData.get('TrckgInd'),
#             "CDTR_NM_VALUE": requestData.get('Cdtr_nm'),
#             "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
#             "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
#             "DBTR_NM_VALUE": requestData.get('Dbtr_nm'),
#             "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
#             "ORGNL_MNDT_STS_VALUE": requestData.get('OrgnlMndt_sts')
#         }

#     filled_data = handler.replace_placeholders(template_data, value_dict)

#     filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
#     filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
#     filled_data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0][0]["AccptncRslt"]["Accptd"] = True
#     headers = {
#         "Content-Type": "application/json",
#         "Content-Length": str(filled_data),
#         "message": "/MandateAcceptanceReportV06"
#     }

#     response = requests.post(
#         f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

#     return response.text
