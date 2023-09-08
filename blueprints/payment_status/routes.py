from flask import render_template
from . import payment_status_bp
from . import payment_status_report_json_handlers
from flask import Flask, request, render_template, jsonify

from functools import wraps

def dynamic_route(url_rule, json_func, xml_func):
    def decorator(func):
        @wraps(func)
        def wrapper(scheme):
            try:
                data = request.get_json()
                if scheme == 'json':
                    return json_func(data)
                elif scheme == 'xml':
                    return xml_func(data)
            except Exception as e:
                return jsonify({"error": str(e)}), 400 
        return wrapper
    return decorator

@payment_status_bp.route('/<scheme>/build', methods=['POST'])
@dynamic_route('<scheme>/build', payment_status_report_json_handlers.buildMessage, payment_status_report_json_handlers.buildMessage)
def build_message(scheme):
    pass

@payment_status_bp.route('/<scheme>/request', methods=['POST'])
@dynamic_route('<scheme>/request', payment_status_report_json_handlers.requestMessage, payment_status_report_json_handlers.requestMessage)
def request_message(scheme):
    pass

