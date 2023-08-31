from flask import Flask, Response, current_app, jsonify
import requests
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import socket
import xml.etree.ElementTree as ET
import struct
import xml.dom.minidom
import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def buildMessage(data, initiator):
    # Construct file path
    template_filename = 'pain.009.001.06_MandateRegist.xml'
    file_path = os.path.join(current_app.root_path,
                             'blueprints', 'mandate','templates', template_filename)

    # Generate unique IDs
    payment_type_key = 'PAYMENT_TYPE'
    initiator_dict = {
        'creditor': paymentData.emandateRegistrationByCreditor,
        'debitor': paymentData.emandateRegistrationByDebitor
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

    payment_dynamic_data = {
        # "INTR_BK_STTLM_DT_VALUE": handler.getCreDt(),
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
        **paymentData.emandateRegistrationByCreditor,
        **paymentData.cdtrData,
        **paymentData.dbtrData,
    }

    # Set the Date
    timestamp_now = datetime.now() + timedelta(days=1)
    timestamp_formatted = timestamp_now.strftime('%Y-%m-%d')
    timestamp_future = timestamp_now + relativedelta(years=1)
    timestamp_future_formatted = timestamp_future.strftime('%Y-%m-%d')
    value_dict['DRTN_FRDT_VALUE'] = timestamp_formatted
    value_dict['DRTN_TODT_VALUE'] = timestamp_future_formatted
    value_dict['FRST_COLLTNDT_VALUE'] = timestamp_formatted
    value_dict['FNL_COLLTNDT_VALUE'] = timestamp_future_formatted

    # Replace placeholders in template data
    filled_data = handler.replace_placeholders_xml(xml_template, value_dict)

    # tags_to_remove = customForm.getlist('tags_to_remove')

    # if tags_to_remove is not None:
    #     handler.remove_tags(filled_data, tags_to_remove)

    # Pretty print
    xml_dom = xml.dom.minidom.parseString(filled_data)
    pretty_xml_content = xml_dom.toprettyxml(indent="  ")

    return pretty_xml_content


def requestMessage(message, initiator):
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
