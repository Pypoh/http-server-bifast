from flask import Flask, Response, current_app, jsonify
from datetime import datetime
import requests
import json
import os
import sys
import handler.general as handler


from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessageRegistration(requestData):
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'prxy.001.001.01_Proxy.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("710")
    generatedMsgId = handler.generateMsgId("710")

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
            "MSGSNDR_AGT_VALUE": requestData.get('MsgSndr_agt'),
            "MSGSNDR_ACCT_ID_VALUE": requestData.get('MsgSndr_acct'),
            "REGN_TP_VALUE": requestData.get('RegnTp'),
            "REGN_PRXY_TP_VALUE": requestData.get('Prxy_tp'),
            "REGN_PRXY_VAL_VALUE": requestData.get('Prxy_val'),
            "PRXYREGN_DSPLNM_VALUE": requestData.get('DsplNm'),
            "PRXYREGN_AGT_NM_VALUE": requestData.get('PrxyRegn_Agt_nm'),
            "PRXYREGN_AGT_ID_VALUE": requestData.get('PrxyRegn_Agt_id'),
            "PRXYREGN_ACCT_ID_VALUE": requestData.get('PrxyRegn_acct'),
            "PRXYREGN_ACCT_TP_VALUE": requestData.get('PrxyRegn_tp'),
            "PRXYREGN_ACCT_NM_VALUE": requestData.get('PrxyRegn_nm'),
            "PRXYREGN_SCNDID_TP_VALUE": requestData.get('ScndId_tp'),
            "PRXYREGN_SCNDID_VAL_VALUE": requestData.get('ScndId_val'),
            "PRXYREGN_STS_VALUE": requestData.get('RegnSts'),
            "SPLMNTR_CSTMR_TP_VALUE": requestData.get('SplmtryData_Cstmr_tp'),
            "SPLMNTR_CSTMR_ID_VALUE": requestData.get('SplmtryData_Cstmr_id'),
            "SPLMNTR_CSTMR_RSNDT_VALUE": requestData.get('SplmtryData_Cstmr_rsdntsts'),
            "SPLMNTR_CSTMR_TWNNM_VALUE": requestData.get('SplmtryData_Cstmr_twnnm')

        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/ProxyRegistrationV01"
    }
    response = requests.post(
        f"{SCHEME_VALUE}{requestData.get('Host_url')}:{requestData.get('Host_port')}", json=filled_data, headers=headers)

    return response.text


def requestMessagePorting():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'prxy.001.001.01_Proxy.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("720")
    generatedMsgId = handler.generateMsgId("720")

    uniqueId = random.randint(00000, 99999)

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "MSGSNDR_AGT_VALUE": BANK_CODE_VALUE,
            "MSGSNDR_ACCT_ID_VALUE": f"1234{uniqueId}",
            "REGN_TP_VALUE": "PORT",
            "REGN_PRXY_TP_VALUE": "02",
            "REGN_PRXY_VAL_VALUE": f"naufal.afif.{uniqueId}@gmail.com",
            "PRXYREGN_DSPLNM_VALUE": f"Naufal Afif {uniqueId}",
            "PRXYREGN_AGT_NM_VALUE": f"Naufal Agent {uniqueId}",
            "PRXYREGN_AGT_ID_VALUE": BANK_CODE_VALUE,
            "PRXYREGN_ACCT_ID_VALUE": f"1234{uniqueId}",
            "PRXYREGN_ACCT_TP_VALUE": "CACC",
            "PRXYREGN_ACCT_NM_VALUE": f"Afif Bunyamin {uniqueId}",
            "PRXYREGN_SCNDID_TP_VALUE": "01",
            "PRXYREGN_SCNDID_VAL_VALUE": f"628521{uniqueId}",
            "PRXYREGN_STS_VALUE": "ACTV",
            "SPLMNTR_CSTMR_TP_VALUE": "01",
            "SPLMNTR_CSTMR_ID_VALUE": f"124123152{uniqueId}",
            "SPLMNTR_CSTMR_RSNDT_VALUE": "01",
            "SPLMNTR_CSTMR_TWNNM_VALUE": "0300"

        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/ProxyRegistrationV01"
    }
    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text


def requestMessageDeactivate():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'prxy.001.001.01_Proxy.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("720")
    generatedMsgId = handler.generateMsgId("720")

    uniqueId = random.randint(00000, 99999)

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": generatedMsgId,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "MSGSNDR_AGT_VALUE": BANK_CODE_VALUE,
            "MSGSNDR_ACCT_ID_VALUE": f"1234{uniqueId}",
            "REGN_TP_VALUE": "PORT",
            "REGN_PRXY_TP_VALUE": "02",
            "REGN_PRXY_VAL_VALUE": f"naufal.afif.{uniqueId}@gmail.com",
            "PRXYREGN_DSPLNM_VALUE": f"Naufal Afif {uniqueId}",
            "PRXYREGN_AGT_NM_VALUE": f"Naufal Agent {uniqueId}",
            "PRXYREGN_AGT_ID_VALUE": BANK_CODE_VALUE,
            "PRXYREGN_ACCT_ID_VALUE": f"1234{uniqueId}",
            "PRXYREGN_ACCT_TP_VALUE": "CACC",
            "PRXYREGN_ACCT_NM_VALUE": f"Afif Bunyamin {uniqueId}",
            "PRXYREGN_SCNDID_TP_VALUE": "01",
            "PRXYREGN_SCNDID_VAL_VALUE": f"628521{uniqueId}",
            "PRXYREGN_STS_VALUE": "ACTV",
            "SPLMNTR_CSTMR_TP_VALUE": "01",
            "SPLMNTR_CSTMR_ID_VALUE": f"124123152{uniqueId}",
            "SPLMNTR_CSTMR_RSNDT_VALUE": "01",
            "SPLMNTR_CSTMR_TWNNM_VALUE": "0300"

        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/ProxyRegistrationV01"
    }
    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text


def requestMessageLookup():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'prxy.003.001.01_ProxyLookup.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("610")
    generatedMsgId = handler.generateMsgId("610")

    uniqueId = random.randint(00000, 99999)

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": ,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "MSGSNDR_AGT_VALUE": BANK_CODE_VALUE,
            "MSGSNDR_ACCT_ID_VALUE": f"1234{uniqueId}",
            "LOOKUP_PRXY_TP_VALUE": "PXRS",
            "LOOKUP_PRXY_ID_VALUE": generatedMsgId,
            "LOOKUP_PRXYRTRVL_TP_VALUE": "02",
            "LOOKUP_PRXYRTRVL_VAL_VALUE": "naufal.afif@ptap.com"

        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/ProxyRegistrationV01"
    }
    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text


def requestMessageEnquiry():
    filePath = os.path.join(
        current_app.config["FORMAT_PATH"], 'prxy.005.001.01_ProxyEnquiry.json')

    generatedBizMsgIdr = handler.generateBizMsgIdr("610")
    generatedMsgId = handler.generateMsgId("610")

    uniqueId = random.randint(00000, 99999)

    with open(filePath, 'r') as file:
        template_data = json.load(file)
        value_dict = {
            "FR_BIC_VALUE": BANK_CODE_VALUE,
            "TO_BIC_VALUE": HUB_CODE_VALUE,
            "BIZ_MSG_IDR_VALUE": generatedBizMsgIdr,
            "CRE_DT_VALUE": handler.getCreDt(),
            "MSG_ID_VALUE": ,
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "MSGSNDR_AGT_VALUE": BANK_CODE_VALUE,
            "MSGSNDR_ACCT_ID_VALUE": f"1234{uniqueId}",
            "NQRY_SCNDID_TP_VALUE": "02",
            "NQRY_SCNDID_VAL_VALUE": "naufal.afif@ptap.com",
        }
    filled_data = handler.replace_placeholders(template_data, value_dict)
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(filled_data),
        "message": "/ProxyRegistrationV01"
    }
    response = requests.post(
        f"{SCHEME_VALUE}{HOST_URL_VALUE}:{HOST_PORT_VALUE}", json=filled_data, headers=headers)

    return response.text
