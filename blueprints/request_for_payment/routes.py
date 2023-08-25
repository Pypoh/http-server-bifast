from flask import render_template
from . import request_for_payment_bp
from . import request_for_pay_json_handlers, request_for_pay_xml_handlers, request_for_pay_reject_json_handlers, request_for_pay_reject_xml_handlers
from flask import Flask, request, render_template, jsonify

build_handlers = {
    'account': {
        'json': request_for_pay_json_handlers.buildMessage,
        # 'xml': request_for_pay_xml_handlers.buildMessage
    },
    # 'proxy': {
    #     'json': credit_transfer_proxy_json_handlers.buildMessage,
    #     'xml': credit_transfer_proxy_xml_handlers.buildMessage
    # },
    'reject_account': {
        'json': request_for_pay_reject_json_handlers.buildMessage,
        # 'xml': request_for_pay_reject_xml_handlers.buildMessage
    },
    # 'reject_proxy': {
    #     'json': credit_transfer_proxy_json_handlers.buildMessage,
    #     'xml': credit_transfer_proxy_xml_handlers.buildMessage
    # },
}
request_handlers = {
    'account': {
        'json': request_for_pay_json_handlers.requestMessage,
        # 'xml': request_for_pay_xml_handlers.requestMessage
    },
    # 'proxy': {
    #     'json': credit_transfer_proxy_json_handlers.requestMessage,
    #     'xml': credit_transfer_proxy_xml_handlers.requestMessage
    # },
    'reject_account': {
        'json': request_for_pay_reject_json_handlers.requestMessage,
        # 'xml': request_for_pay_reject_xml_handlers.requestMessage
    },
    # 'reject_proxy': {
    #     'json': credit_transfer_proxy_json_handlers.requestMessage,
    #     'xml': credit_transfer_proxy_xml_handlers.requestMessage
    # },
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

@request_for_payment_bp.route('/<type>/<scheme>/build', methods=['POST'])
def buildMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'build', data)

@request_for_payment_bp.route('/<type>/<scheme>/request', methods=['POST'])
def requestMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'request', data)