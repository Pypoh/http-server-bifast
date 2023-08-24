from flask import render_template
from . import account_enquiry_bp
from . import accountEnquiryHandler
from flask import Flask, request, render_template, jsonify

# @app.route('/AccountEnquiryOFI', methods=['POST'])
# def aeHandlerOFI():
#     if request.method == 'POST':
#         try:
#             data = request.get_json()
#             # print("Received JSON data:", data)
#             response_data = {
#                 "status": "success",
#                 "message": "Request processed successfully",
#             }
#             # return jsonify(response_data), 200
#         except Exception as e:
#             pass
#             # return jsonify({"error": "Invalid JSON data"}), 400
#             # return jsonify({"error": f"{e}"}), 400

#         # return accountEnquiryHandler.requestMessage(request.form)
#         return accountEnquiryHandler.requestMessage(data)

@account_enquiry_bp.route('/build', methods=['POST'])
def buildMessage():
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "Invalid JSON data"}), 400

        return accountEnquiryHandler.buildMessage(data)

@account_enquiry_bp.route('/request', methods=['POST'])
def requestMessage():
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "Invalid JSON data"}), 400

        return accountEnquiryHandler.requestMessage(data)