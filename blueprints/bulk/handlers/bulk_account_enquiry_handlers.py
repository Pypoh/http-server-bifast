from flask import Flask, Response, current_app, jsonify
import requests
import handler.general as handler
from datetime import datetime
import json
import os
import sys
import socket
import xml.etree.ElementTree as ET
import struct
import xml.dom.minidom
import random

import repository.data as generalData
import repository.payment as paymentData

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def buildMessage(data):
    # Construct file path
    template_filename = 'pacs.008.001.10_BulkAccountEnquiry.xml'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'bulk', 'templates', template_filename)

    # Declare bulk message variable
    bulkMessage = ""

    # Get transaction count
    nbOfTxs = int(data['NB_OF_TXS'])
    trxCount = 0
    for x in range(1, nbOfTxs + 1):
        # Generate unique IDs
        payment_type = paymentData.accountEnquiry.get('PAYMENT_TYPE')
        dbtr_agt = generalData.sampleData.get('DBTRAGT')
        generated_biz_msg_idr = handler.generateBizMsgIdr(
            dbtr_agt, payment_type)
        generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)
        generated_bulk_id = handler.generateBulkId()

        unique_id = {
            "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
            "MSG_ID_VALUE": generated_msg_id,
            "END_TO_END_ID_VALUE": generated_biz_msg_idr,
            "TX_ID_VALUE": generated_msg_id,
        }

        base_dynamic_data = {
            "CRE_DT_VALUE": handler.getCreDt(),
            "CRE_DT_TM_VALUE": handler.getCreDtTm(),
            "FR_BIC_VALUE": dbtr_agt
        }

        bulk_id_data = {
            "BLK_ID_HEADER_VALUE": generated_bulk_id,
            "BLK_ID_BODY_VALUE": generated_bulk_id,
            "NB_OF_TXS_HEADER_VALUE": nbOfTxs
        }

        payment_dynamic_data = {
            "INTR_BK_STTLM_DT_VALUE": handler.getCreDt(),
        }

        # Load the XML file as an ElementTree
        with open(file_path, 'r') as file:
            xml_template = file.read()
            
        # Create base xml
        # root = xml_template.getroot()
        # bulk = ET.Element("Bulk")

        # Create value dictionary for placeholders
        value_dict = {
            **unique_id,
            **base_dynamic_data,
            **bulk_id_data,
            **payment_dynamic_data,
            **paymentData.base,
            **paymentData.accountEnquiry,
            **paymentData.cdtrData,
            **paymentData.dbtrData,
            **paymentData.splmtryData
        }

        # Replace placeholders in template data
        filled_data = handler.replace_placeholders_xml(
            xml_template, value_dict)

        # Pretty print
        xml_dom = xml.dom.minidom.parseString(filled_data)
        pretty_xml_content = xml_dom.toprettyxml(indent="  ")
        
        # Append message
        bulkMessage = bulkMessage + pretty_xml_content
        # bulk.append(pretty_xml_content)

    # tree = ET.ElementTree(bulk)
    # tree.write(f"{formatted_timestamp}.0200{uniqueId}-etc.xml")
    # busmsg = tree.find("BusMsg")

    bulk_result = buildFile(bulkMessage)
    
    return bulk_result


def buildFile(message):
    # formatted_date = datetime.now().strftime('%Y%m%d')
    formatted_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    generated_file_name = random.randint(1000, 9999)
    template_filename = f"{formatted_timestamp}.0200{generated_file_name}-etc.xml"
    file_path = os.path.join(current_app.root_path,
                             'bulk_result', template_filename)
    
    # Write the XML string to the file
    with open(file_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(message)
    
    return file_path 


def requestMessage(filepath):
    

    return filepath
