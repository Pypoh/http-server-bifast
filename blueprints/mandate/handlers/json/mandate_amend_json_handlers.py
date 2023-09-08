from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE

def buildMessage(data, initiator):
    # Construct file path
    template_filename = 'pain.010.001.06_MandateAmend.json'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'mandate', 'templates', template_filename)

    # Generate unique IDs
    payment_type_key = 'PAYMENT_TYPE'
    initiator_dict = {
        'creditor': paymentData.emandateAmendmentByCreditor,
        'debitor': paymentData.emandateAmendmentByDebitor
    }
    payment_type = initiator_dict.get(initiator, {}).get(payment_type_key)
    agent_key = 'CDTRAGT' if initiator == 'creditor' else 'DBTRAGT'
    agent_value = generalData.sampleData.get(agent_key, None)
    generated_biz_msg_idr = handler.generateBizMsgIdr(agent_value, payment_type)
    generated_msg_id = handler.generateMsgId(agent_value, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "MNDT_REQ_ID_VALUE": generated_biz_msg_idr,
    }
    
    base_dynamic_data = {
        "CRE_DT_VALUE": handler.getCreDt(),
        "CRE_DT_TM_VALUE": handler.getCreDtTm(),
        "FR_BIC_VALUE": agent_value
    }

    # Load template data
    with open(file_path, 'r') as file:
        template_data = json.load(file)

    DRTN_FRDT_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["FrDt"]
    DRTN_TODT_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Drtn"]["ToDt"]
    FRST_COLLTNDT_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FrstColltnDt"]
    FNL_COLLTNDT_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["FnlColltnDt"]
    MNDT_MNDTID_VALUE = data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtId"]
    
    original_data = {
        "MNDT_MNDTID_VALUE": MNDT_MNDTID_VALUE,
        "ORGNLMNDT_MNDTID_VALUE": MNDT_MNDTID_VALUE,
        "ORGNLMNDT_REQ_ID_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MndtReqId"],
        "ORGNLMNDT_LCLINSTRM_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Tp"]["LclInstrm"]["Prtry"],
        "ORGNLMNDT_CTGYPURP_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Tp"]["CtgyPurp"]["Prtry"],
        "ORGNLMNDT_OCRNCS_SEQTP_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["SeqTp"],
        "ORGNLMNDT_OCRNCS_FRQCY_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Frqcy"]["Prd"]["Tp"],
        "ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"],
        "ORGNLMNDT_DRTN_FRDT_VALUE": DRTN_FRDT_VALUE,
        "ORGNLMNDT_DRTN_TODT_VALUE": DRTN_TODT_VALUE,
        "ORGNLMNDT_FRST_COLLTNDT_VALUE": FRST_COLLTNDT_VALUE,
        "ORGNLMNDT_FNL_COLLTNDT_VALUE": FNL_COLLTNDT_VALUE,
        "ORGNLMNDT_TRCKGIND_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"],
        "ORGNLMNDT_FRST_COLLTNAMT_CCY_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["FrstColltnAmt"]["Ccy"],
        "ORGNLMNDT_FRST_COLLTNAMT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["FrstColltnAmt"]["value"],
        "ORGNLMNDT_COLLTNAMT_CCY_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["ColltnAmt"]["Ccy"],
        "ORGNLMNDT_COLLTNAMT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["ColltnAmt"]["value"],
        "ORGNLMNDT_MAX_AMT_CCY_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MaxAmt"]["Ccy"],
        "ORGNLMNDT_MAX_AMT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MaxAmt"]["value"],
        "ORGNLMNDT_MNDT_RSN_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Rsn"]["Prtry"],
        "ORGNLMNDT_CDTR_NM_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Cdtr"]["Nm"],
        "ORGNLMNDT_CDTR_ORG_ID_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Cdtr"]["Id"]["OrgId"]["Othr"][0]["Id"],
        "ORGNLMNDT_CDTR_ACCT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["CdtrAcct"]["Id"]["Othr"]["Id"],
        "ORGNLMNDT_CDTR_ACCT_TP_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["CdtrAcct"]["Tp"]["Prtry"],
        "ORGNLMNDT_CDTR_ACCT_NM_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["CdtrAcct"]["Nm"],
        "ORGNLMNDT_CDTR_AGT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["CdtrAgt"]["FinInstnId"]["Othr"]["Id"],
        "ORGNLMNDT_DBTR_NM_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Dbtr"]["Nm"],
        "ORGNLMNDT_DBTR_PRVT_ID_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Dbtr"]["Id"]["PrvtId"]["Othr"][0]["Id"],
        "ORGNLMNDT_DBTR_ACCT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["DbtrAcct"]["Id"]["Othr"]["Id"],
        "ORGNLMNDT_DBTR_ACCT_TP_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["DbtrAcct"]["Tp"]["Prtry"],
        "ORGNLMNDT_DBTR_ACCT_NM_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["DbtrAcct"]["Nm"],
        "ORGNLMNDT_DBTR_AGT_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["DbtrAgt"]["FinInstnId"]["Othr"]["Id"],
        "ORGNLMNDT_RFRD_DOC_CDTR_REF_VALUE": data["BusMsg"]["Document"]["MndtAccptncRpt"]["UndrlygAccptncDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["RfrdDoc"][0]["CdtrRef"],
    }

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **base_dynamic_data,
        **original_data,
        **paymentData.base,
        **paymentData.emandateAmendmentByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # # Set the Date
    # timestamp_now = datetime.now() - timedelta(days=7)
    # timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    # timestamp_future = datetime.now() - timedelta(days=3)
    # timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    # value_dict['DRTN_FRDT_VALUE'] = timestamp_formatted
    # value_dict['DRTN_TODT_VALUE'] = timestamp_future_formatted
    # value_dict['FRST_COLLTNDT_VALUE'] = timestamp_formatted
    # value_dict['FNL_COLLTNDT_VALUE'] = timestamp_future_formatted
        
    # timestamp_now = datetime.now()
    # timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    # timestamp_future = timestamp_now + relativedelta(years=1)
    # timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    # value_dict['DRTN_FRDT_VALUE'] = timestamp_formatted
    # value_dict['DRTN_TODT_VALUE'] = timestamp_future_formatted
    # value_dict['FRST_COLLTNDT_VALUE'] = timestamp_formatted
    # value_dict['FNL_COLLTNDT_VALUE'] = timestamp_future_formatted
    
    value_dict['DRTN_FRDT_VALUE'] = DRTN_FRDT_VALUE
    value_dict['DRTN_TODT_VALUE'] = DRTN_TODT_VALUE
    value_dict['FRST_COLLTNDT_VALUE'] = FRST_COLLTNDT_VALUE
    value_dict['FNL_COLLTNDT_VALUE'] = FNL_COLLTNDT_VALUE
    value_dict['MNDT_MNDTID_VALUE'] = MNDT_MNDTID_VALUE

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders(template_data, value_dict)

    # print(value_dict, file=sys.stderr)

    # Convert payment data
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        value_dict.get('OCRNCS_CNTPERPRD_VALUE')))
    # filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["FrstColltnAmt"]["value"] = float(
    #     value_dict.get('FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["ColltnAmt"]["value"] = float(
        value_dict.get('COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["Mndt"]["MaxAmt"]["value"] = float(
        value_dict.get('MAX_AMT_VALUE'))

    # Convert original payment data
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = int(float(
        value_dict.get('ORGNLMNDT_OCRNCS_CNTPERPRD_VALUE')))
    # filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["FrstColltnAmt"]["value"] = float(
    #     value_dict.get('ORGNLMNDT_FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["ColltnAmt"]["value"] = float(
        value_dict.get('ORGNLMNDT_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtAmdmntReq"]["UndrlygAmdmntDtls"][0]["OrgnlMndt"]["OrgnlMndt"]["MaxAmt"]["value"] = float(
        value_dict.get('ORGNLMNDT_MAX_AMT_VALUE'))

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)
    return filled_data


def requestMessage(message, initiator):
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(message))),
        "message": "/MandateAmendmentRequestV06"
    }

    # Get Agent
    agent_key = 'CDTR_PORT' if initiator == 'creditor' else 'DBTR_PORT'
    agent_value = generalData.sampleData.get(agent_key, None)

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{agent_value}"
    response = requests.post(host_url, json=message, headers=headers)
    
    return response.text

