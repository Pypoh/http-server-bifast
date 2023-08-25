from flask import render_template
from . import credit_transfer_bp
from . import credit_transfer_json_handlers, credit_transfer_proxy_json_handlers, credit_transfer_reversal_json_handlers, credit_transfer_rfp_json_handlers
from . import credit_transfer_xml_handlers, credit_transfer_proxy_xml_handlers, credit_transfer_reversal_xml_handlers, credit_transfer_rfp_xml_handlers
from flask import Flask, request, render_template, jsonify

build_handlers = {
    'account': {
        'json': credit_transfer_json_handlers.buildMessage,
        'xml': credit_transfer_xml_handlers.buildMessage
    },
    'proxy': {
        'json': credit_transfer_proxy_json_handlers.buildMessage,
        'xml': credit_transfer_proxy_xml_handlers.buildMessage
    },
    'reversal': {
        'json': credit_transfer_reversal_json_handlers.buildMessage,
        'xml': credit_transfer_reversal_xml_handlers.buildMessage
    },
    'rfp': {
        'json': credit_transfer_rfp_json_handlers.buildMessage,
        'xml': credit_transfer_rfp_xml_handlers.buildMessage
    }
}
request_handlers = {
    'account': {
        'json': credit_transfer_json_handlers.requestMessage,
        'xml': credit_transfer_xml_handlers.requestMessage
    },
    'proxy': {
        'json': credit_transfer_proxy_json_handlers.requestMessage,
        'xml': credit_transfer_proxy_xml_handlers.requestMessage
    },
    'reversal': {
        'json': credit_transfer_reversal_json_handlers.requestMessage,
        'xml': credit_transfer_reversal_xml_handlers.requestMessage
    },
    'rfp': {
        'json': credit_transfer_rfp_json_handlers.requestMessage,
        'xml': credit_transfer_rfp_xml_handlers.requestMessage
    }
}

def process_message(type, scheme, action, data):
    try:
        if action == 'build':
            handler = build_handlers.get(type, {}).get(scheme)
        elif action == 'request':
            handler = request_handlers.get(type, {}).get(scheme)
        if handler:
            return handler(data)
        return jsonify({"error": "Invalid type or scheme"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@credit_transfer_bp.route('/<type>/<scheme>/build', methods=['POST'])
def buildMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'build', data)

@credit_transfer_bp.route('/<type>/<scheme>/request', methods=['POST'])
def requestMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'request', data)