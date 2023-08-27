from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime, timedelta
import socket
import xml.etree.ElementTree as ET
import struct
import xml.dom.minidom

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def buildMessage(data):
    # Construct file path
    template_filename = 'pain.013.001.08_RequestForPay.xml'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'request_for_payment', 'templates', template_filename)

    # Generate unique IDs
    payment_type = paymentData.requestForPaymentByProxy.get('PAYMENT_TYPE')
    cdtr_agt = generalData.sampleData.get('CDTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(cdtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(cdtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "END_TO_END_ID_VALUE": generated_biz_msg_idr,
        "TX_ID_VALUE": generated_msg_id,
    }

    # Load template data
    with open(file_path, 'r') as file:
        xml_template = file.read()

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **paymentData.requestForPaymentByAccount,
        **paymentData.base,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
        **paymentData.splmtryData
    }

    # Set the Date
    timestamp_now = datetime.now()
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_future = timestamp_now + timedelta(days=14)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    value_dict['REQD_EXCTN_DT_VALUE'] = timestamp_formatted
    value_dict['XPRY_DT_VALUE'] = timestamp_future_formatted

    # Parse the XML content
    root = ET.fromstring(xml_template)

    # Namespace dictionary
    ns = {
        'ns0': 'urn:iso',
        'ns2': 'urn:iso:std:iso:20022:tech:xsd:pain.013.001.08'
    }

    # Find the DbtrAcct element
    dbtr_acct = root.find('.//ns2:DbtrAcct', namespaces=ns)

    # Create the Prxy element
    prxy_element = ET.Element('{urn:iso:std:iso:20022:tech:xsd:pain.013.001.08}Prxy')

    # Create child elements for Prxy
    tp_element = ET.SubElement(prxy_element, '{urn:iso:std:iso:20022:tech:xsd:pain.013.001.08}Tp')
    prtry_element = ET.SubElement(tp_element, '{urn:iso:std:iso:20022:tech:xsd:pain.013.001.08}Prtry')
    proxy_tp = generalData.sampleData.get('DBTRACCT_PRXY_TYPE')
    prtry_element.text = proxy_tp

    id_element = ET.SubElement(prxy_element, '{urn:iso:std:iso:20022:tech:xsd:pain.013.001.08}Id')
    proxy_id = generalData.sampleData.get('DBTRACCT_PRXY_ID')
    id_element.text = proxy_id

    # Add the Prxy element to DbtrAcct
    dbtr_acct.append(prxy_element)

    # Convert the modified XML back to a string
    modified_xml = ET.tostring(root, encoding='unicode')

    filled_data = handler.replace_placeholders_xml(modified_xml, value_dict)

    # Pretty print
    xml_dom = xml.dom.minidom.parseString(filled_data)
    pretty_xml_content = xml_dom.toprettyxml(indent="  ")

    return pretty_xml_content


def requestMessage(message):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/CreditorPaymentActivationRequestV08"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('CDTR_PORT')}"
    response = requests.post(host_url, json=message, headers=headers)

    return response.text


# def requestMessageByAccount(isProxy=False):
#     # Construct file path
#     template_filename = 'pain.013.001.08_RequestForPay.json'
#     file_path = os.path.join(
#         current_app.config["FORMAT_PATH"], template_filename)

#     # Generate unique IDs
#     payment_type = paymentData.creditTransfer.get('PAYMENT_TYPE')
#     dbtr_agt = generalData.sampleData.get('DBTRAGT')
#     generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
#     generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

#     unique_id = {
#         "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
#         "MSG_ID_VALUE": generated_msg_id,
#         "END_TO_END_ID_VALUE": generated_biz_msg_idr,
#         "TX_ID_VALUE": generated_msg_id,
#     }

#     # Load template data
#     with open(file_path, 'r') as file:
#         template_data = json.load(file)

#     # Create value dictionary for placeholders
#     value_dict = {
#         **unique_id,
#         **paymentData.base,
#         **paymentData.requestForPaymentByAccount,
#         **paymentData.cdtrData,
#         **paymentData.dbtrData,
#         **paymentData.splmtryData
#     }

#     if (isProxy):
#         value_dict = {
#             **value_dict,
#             **paymentData.requestForPaymentByProxy,
#         }
#     else:
#         value_dict = {
#             **value_dict,
#             **paymentData.requestForPaymentByAccount,
#         }

#     # with open(filePath, 'r') as file:
#     #     template_data = json.load(file)
#     #     value_dict = {
#     #         "FR_BIC_VALUE": requestData.get('Fr'),
#     #         "TO_BIC_VALUE": requestData.get('To'),
#     #         "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
#     #         "MSG_DEF_IDR_VALUE": requestData.get('MsgDefIdr'),
#     #         "BIZ_SVC_VALUE": requestData.get('BizSvc'),
#     #         "CRE_DT_VALUE": handler.getCreDt(),
#     #         "CPYDPLCT_VALUE": requestData.get('CpyDplct'),
#     #         "PSSBLDPLCT_VALUE": requestData.get('PssblDplct'),
#     #         "MSG_ID_VALUE": generatedMsgId,
#     #         "CRE_DT_TM_VALUE": handler.getCreDtTm(),
#     #         "NM_OF_TXS_VALUE": requestData.get('NbOfTxs'),
#     #         "INITG_PTY_NM_VALUE": requestData.get('InitgPty_nm'),
#     #         "PSTLADR_CTRY_VALUE": requestData.get('InitgPty_pstladr'),
#     #         "PMTINF_PMTMTD_VALUE": requestData.get('PmtMtd'),
#     #         "PMTTPINF_CTGYPURP_VALUE": requestData.get('CtgyPurp'),
#     #         "REQD_EXCTN_DT_VALUE": requestData.get('ReqdExctnDt'),
#     #         "XPRY_DT_VALUE": requestData.get('XpryDt'),
#     #         "DBTR_ACCT_VALUE": requestData.get('DbtrAcct_value'),
#     #         "DBTR_AGT_VALUE": requestData.get('DbtrAgt'),
#     #         "END_TO_END_ID_VALUE": generatedBizMsgIdr,
#     #         "INSTDAMT_VALUE": requestData.get('InstdAmt_value'),
#     #         "INSTDAMT_CCY_VALUE": requestData.get('InstdAmt_ccy'),
#     #         "CHRGBR_VALUE": requestData.get('ChrgBr'),
#     #         "CDTR_AGT_VALUE": requestData.get('CdtrAgt'),
#     #         "CDTR_ORG_ID_VALUE": requestData.get('Cdtr_orgid'),
#     #         "CDTR_ACCT_VALUE": requestData.get('CdtrAcct_value'),
#     #         "CDTR_ACCT_TP_VALUE": requestData.get('CdtrAcct_type'),
#     #         "CDTR_ACCT_NM_VALUE": requestData.get('CdtrAcct_nm'),
#     #         "SPLMNTR_CDTR_TP_VALUE": requestData.get('SplmtryData_Cdtr_tp'),
#     #         "SPLMNTR_CDTR_RSDNTSTS_VALUE": requestData.get('SplmtryData_Cdtr_rsdntsts'),
#     #         "SPLMNTR_CDTR_TWNNM_VALUE": requestData.get('SplmtryData_Cdtr_twnnm'),
#     #     }

#     # Replace placeholders in template data
#     filled_data = handler.replace_placeholders(template_data, value_dict)
#     filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = float(
#         value_dict.get('INSTD_AMT_VALUE'))
#     filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

#     # Prepare headers
#     headers = {
#         "Content-Type": "application/json",
#         "Content-Length": str(len(json.dumps(filled_data))),
#         "message": "/CreditorPaymentActivationRequestV08"
#     }

#     # Send POST request
#     host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('HOST_PORT')}"
#     response = requests.post(host_url, json=filled_data, headers=headers)

#     return response.text


# def requestMessageByProxy(requestData):
#     # Construct file path
#     template_filename = 'pain.013.001.08_RequestForPay.json'
#     file_path = os.path.join(
#         current_app.config["FORMAT_PATH"], template_filename)

#     # Generate unique IDs
#     payment_type = paymentData.creditTransfer.get('PAYMENT_TYPE')
#     dbtr_agt = generalData.sampleData.get('DBTRAGT')
#     generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
#     generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

#     unique_id = {
#         "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
#         "MSG_ID_VALUE": generated_msg_id,
#         "END_TO_END_ID_VALUE": generated_biz_msg_idr,
#         "TX_ID_VALUE": generated_msg_id,
#     }

#     # Load template data
#     with open(file_path, 'r') as file:
#         template_data = json.load(file)

#     # Create value dictionary for placeholders
#     value_dict = {
#         **unique_id,
#         **paymentData.base,
#         **paymentData.requestForPaymentByAccount,
#         **paymentData.cdtrData,
#         **paymentData.dbtrData,
#         **paymentData.splmtryData
#     }

#     # Replace placeholders in template data
#     filled_data = handler.replace_placeholders(template_data, value_dict)
#     filled_data["BusMsg"]["Document"]["CdtrPmtActvtnReq"]["PmtInf"][0]["CdtTrfTx"][0]["Amt"]["InstdAmt"]["value"] = float(
#         value_dict.get('INSTD_AMT_VALUE'))
#     filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False

#     # filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct'].setdefault(
#     #     'Prxy', {})
#     # filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy'].setdefault('Tp', {
#     # })
#     # filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy']['Tp']['Prtry'] = requestData.get(
#     #     'DbtrAcct_Prxy_tp')
#     # filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy']['Id'] = requestData.get(
#     #     'DbtrAcct_Prxy_id')

#     # Set proxy information
#     dbtr_acct_prxy = filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct'].setdefault(
#         'Prxy', {}).setdefault('Tp', {})
#     dbtr_acct_prxy['Prtry'] = requestData.get('DbtrAcct_Prxy_tp')
#     filled_data['BusMsg']['Document']['CdtrPmtActvtnReq']['PmtInf'][0]['DbtrAcct']['Prxy']['Id'] = requestData.get(
#         'DbtrAcct_Prxy_id')

#     headers = {
#         "Content-Type": "application/json",
#         "Content-Length": str(len(json.dumps(filled_data))),
#         "message": "/CreditorPaymentActivationRequestV08"
#     }

#     # Send POST request
#     host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('HOST_PORT')}"
#     response = requests.post(host_url, json=filled_data, headers=headers)

#     return response.text


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
