from flask import render_template
from . import direct_debit_bp
from . import direct_debit_json_handler
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

@direct_debit_bp.route('/<scheme>/build', methods=['POST'])
@dynamic_route('<scheme>/build', direct_debit_json_handler.buildMessage, direct_debit_json_handler.buildMessage)
def build_message(scheme):
    pass

@direct_debit_bp.route('/<scheme>/request', methods=['POST'])
@dynamic_route('<scheme>/request', direct_debit_json_handler.requestMessage, direct_debit_json_handler.requestMessage)
def request_message(scheme):
    pass

