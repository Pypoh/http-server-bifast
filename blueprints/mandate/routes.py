from flask import render_template
from . import mandate_bp
from blueprints.mandate.handlers.json import (
    mandate_regist_json_handlers, mandate_approve_json_handlers, mandate_amend_json_handlers, mandate_enquiry_json_handler)
from blueprints.mandate.handlers.xml import mandate_regist_xml_handlers
from flask import Flask, request, render_template, jsonify

build_handlers = {
    'regist': {
        'json': mandate_regist_json_handlers.buildMessage,
        'xml': mandate_regist_xml_handlers.buildMessage
    },
    'approve': {
        'json': mandate_approve_json_handlers.buildMessage,
        'xml': mandate_approve_json_handlers.buildMessage
    },
    'amend': {
        'json': mandate_amend_json_handlers.buildMessage,
        'xml': mandate_amend_json_handlers.buildMessage
    },
    'enquiry': {
        'json': mandate_enquiry_json_handler.buildMessage,
        'xml': mandate_enquiry_json_handler.buildMessage
    },
}
request_handlers = {
    'regist': {
        'json': mandate_regist_json_handlers.requestMessage,
        'xml': mandate_regist_json_handlers.requestMessage
    },
    'approve': {
        'json': mandate_approve_json_handlers.requestMessage,
        'xml': mandate_approve_json_handlers.requestMessage
    },
    'amend': {
        'json': mandate_amend_json_handlers.requestMessage,
        'xml': mandate_amend_json_handlers.requestMessage
    },
    'enquiry': {
        'json': mandate_enquiry_json_handler.requestMessage,
        'xml': mandate_enquiry_json_handler.requestMessage
    },
}


def process_message(type, scheme, action, data, initiator):
    try:
        if action == 'build':
            handler = build_handlers.get(type, {}).get(scheme)
        elif action == 'request':
            handler = request_handlers.get(type, {}).get(scheme)
        if handler:
            return handler(data, initiator)
        return jsonify({"error": "Invalid type or scheme"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@mandate_bp.route('/<type>/<initiator>/<scheme>/build', methods=['POST'])
def buildMessage(type, scheme, initiator):
    data = request.get_json()
    return process_message(type, scheme, 'build', data, initiator)


@mandate_bp.route('/<type>/<initiator>/<scheme>/request', methods=['POST'])
def requestMessage(type, scheme, initiator):
    data = request.get_json()
    return process_message(type, scheme, 'request', data, initiator)
