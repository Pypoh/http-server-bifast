from flask import render_template
from . import account_enquiry_bp
from . import json_handler, xml_handler
from flask import Flask, request, render_template, jsonify

# @account_enquiry_bp.route('/<scheme>/build', methods=['POST'])
# def buildMessage(scheme):
#     try:
#         data = request.get_json()
#         if scheme == 'json':
#             return json_handler.buildMessage(data)
#         elif scheme == 'xml':
#             return xml_handler.buildMessage(data)
#     except Exception as e:
#         return jsonify({"error": f"{e}"}), 400


# @account_enquiry_bp.route('/<scheme>/request', methods=['POST'])
# def requestMessage(scheme):
#     try:
#         data = request.get_json()
#         if scheme == 'json':
#             return json_handler.requestMessage(data)
#         elif scheme == 'xml':
#             return xml_handler.requestMessage(data)
#     except Exception as e:
#         return jsonify({"error": f"{e}"}), 400


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

@account_enquiry_bp.route('/<scheme>/build', methods=['POST'])
@dynamic_route('<scheme>/build', json_handler.buildMessage, xml_handler.buildMessage)
def build_message(scheme):
    pass

@account_enquiry_bp.route('/<scheme>/request', methods=['POST'])
@dynamic_route('<scheme>/request', json_handler.requestMessage, xml_handler.requestMessage)
def request_message(scheme):
    pass

