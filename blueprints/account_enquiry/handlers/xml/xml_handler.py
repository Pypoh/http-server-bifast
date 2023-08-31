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

import repository.data as generalData
import repository.payment as paymentData

from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def buildMessage(requestData):
    # Construct file path
    template_filename = 'pacs.008.001.10_AccountEnquiry.xml'
    # template_filename = 'pacs.008.001.10_BulkAccountEnquiry.xml'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'account_enquiry','templates', template_filename)

     # Generate unique IDs
    payment_type = paymentData.accountEnquiry.get('PAYMENT_TYPE')
    dbtr_agt = generalData.sampleData.get('DBTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(dbtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(dbtr_agt, payment_type)

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
    
    payment_dynamic_data = {
        "INTR_BK_STTLM_DT_VALUE": handler.getCreDt(),
    }

    # Load the XML file as an ElementTree
    with open(file_path, 'r') as file:
        xml_template = file.read()

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
        **base_dynamic_data,
        **payment_dynamic_data,
        **paymentData.base,
        **paymentData.accountEnquiry,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
        **paymentData.splmtryData
    }

    
    # Replace placeholders in template data
    filled_data = handler.replace_placeholders_xml(xml_template, value_dict)

    # tags_to_remove = customForm.getlist('tags_to_remove')

    # if tags_to_remove is not None:
    #     handler.remove_tags(filled_data, tags_to_remove)

    # Pretty print
    xml_dom = xml.dom.minidom.parseString(filled_data)
    pretty_xml_content = xml_dom.toprettyxml(indent="  ")

    return pretty_xml_content


def requestMessage(message):
    message_length = len(message)
    header = struct.pack('!I', message_length)
    print(message)
    message_with_header = header + message.encode('utf-8')

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('10.170.137.115', 18908))

    # Send the XML message to the server
    client_socket.send(message_with_header)

    # Loop to wait for the server's response
    while True:
        header = client_socket.recv(4)
        message_length = struct.unpack('!I', header)[0]

        # Step 2: Read the message bytes
        message_data = client_socket.recv(message_length)

        # Step 3: Decode and process the message
        decoded_message = message_data.decode('utf-8')
        # print("Received message:", decoded_message)
        break

        # Check if the loop should continue
        if decoded_message == "exit":
            break

    # Close the socket connection
    client_socket.close()

     # Pretty print
    xml_dom = xml.dom.minidom.parseString(decoded_message)
    pretty_xml_content = xml_dom.toprettyxml(indent="  ")

    return pretty_xml_content