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
import handler.general as handler
import repository.data as generalData
import repository.payment as paymentData
from config.bankConfig import BANK_CODE_VALUE, HUB_CODE_VALUE, RFI_BANK_CODE_VALUE
from config.serverConfig import SCHEME_VALUE, HOST_URL_VALUE, HOST_PORT_VALUE


def requestMessage(customForm=None):
    # Construct file path
    template_filename = 'pain.009.001.06_MandateRegist.json'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

    # Generate unique IDs
    payment_type = paymentData.emandateRegistrationByCreditor.get(
        'PAYMENT_TYPE')
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

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
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
    filled_data = handler.replace_placeholders(template_data, value_dict)
    filled_data["BusMsg"]["AppHdr"]["PssblDplct"] = False
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["TrckgInd"] = True
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["FrstColltnAmt"]["value"] = float(
        value_dict.get('FRST_COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["ColltnAmt"]["value"] = float(
        value_dict.get('COLLTNAMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["MaxAmt"]["value"] = float(
        value_dict.get('MAX_AMT_VALUE'))
    filled_data["BusMsg"]["Document"]["MndtInitnReq"]["Mndt"][0]["Ocrncs"]["Frqcy"]["Prd"]["CntPerPrd"] = float(
        value_dict.get('OCRNCS_CNTPERPRD_VALUE'))

    tags_to_remove = customForm.getlist('tags_to_remove')
    # print(f'Tag Found: {tags_to_remove}')

    if tags_to_remove is not None:
        handler.remove_tags(filled_data, tags_to_remove)

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(filled_data))),
        "message": "/MandateInitiationRequestV06"
    }

    # Send POST request
    host_url = f"{SCHEME_VALUE}{generalData.sampleData.get('HOST_URL')}:{generalData.sampleData.get('CDTR_PORT')}"
    response = requests.post(host_url, json=filled_data, headers=headers)

    return response.text


def requestMessageXml(customForm=None):
    # Construct file path
    template_filename = 'pain.009.001.06_MandateRegist.xml'
    file_path = os.path.join(
        current_app.config["FORMAT_PATH"], template_filename)

    # Generate unique IDs
    payment_type = paymentData.emandateRegistrationByCreditor.get(
        'PAYMENT_TYPE')
    cdtr_agt = generalData.sampleData.get('CDTRAGT')
    generated_biz_msg_idr = handler.generateBizMsgIdr(cdtr_agt, payment_type)
    generated_msg_id = handler.generateMsgId(cdtr_agt, payment_type)

    unique_id = {
        "BIZ_MSG_IDR_VALUE": generated_biz_msg_idr,
        "MSG_ID_VALUE": generated_msg_id,
        "MNDT_REQ_ID_VALUE": generated_biz_msg_idr,
    }

    # Load the XML file as an ElementTree
    with open(file_path, 'r') as file:
        xml_template = file.read()

    # Create value dictionary for placeholders
    value_dict = {
        **unique_id,
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

    tags_to_remove = customForm.getlist('tags_to_remove')

    if tags_to_remove is not None:
        handler.remove_tags(filled_data, tags_to_remove)

    # Print filled data (for debugging)
    # print(filled_data, file=sys.stderr)

    message_length = len(filled_data)
    header = struct.pack('!I', message_length)
    message_with_header = header + filled_data.encode('utf-8')

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('10.170.137.115', 18907))

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
        print("Received message:", decoded_message)
        break

        # Check if the loop should continue
        if decoded_message == "exit":
            break

    # Close the socket connection
    client_socket.close()

    # return response.text
