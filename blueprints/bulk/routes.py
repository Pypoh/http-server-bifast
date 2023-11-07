from flask import render_template
from . import bulk_bp

from blueprints.bulk.handlers import bulk_account_enquiry_handlers
from flask import Flask, request, render_template, jsonify

build_handlers = {
    'account_enquiry': {
        'json': bulk_account_enquiry_handlers.buildMessage,
        'xml': bulk_account_enquiry_handlers.buildMessage
    },
    'credit_transfer_account': {
        'json': bulk_account_enquiry_handlers.buildMessage,
        'xml': bulk_account_enquiry_handlers.buildMessage
    }
}
request_handlers = {
    'account_enquiry': {
        'json': bulk_account_enquiry_handlers.requestMessage,
        'xml': bulk_account_enquiry_handlers.requestMessage
    },
    'credit_transfer_account': {
        'json': bulk_account_enquiry_handlers.requestMessage,
        'xml': bulk_account_enquiry_handlers.requestMessage
    },
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


@bulk_bp.route('/<type>/<scheme>/build', methods=['POST'])
def buildMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'build', data)


@bulk_bp.route('/<type>/<scheme>/request', methods=['POST'])
def requestMessage(type, scheme):
    data = request.get_json()
    return process_message(type, scheme, 'request', data)
