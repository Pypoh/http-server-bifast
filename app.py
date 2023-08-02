from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, request, render_template, jsonify
import handler.general as handler
import handler.message.accountEnquiryHandler as accountEnquiryHandler
import handler.message.creditTransferHandler as creditTransferHandler
import handler.message.creditTransferReversalHandler as creditTransferReversalHandler
import handler.message.creditTransferProxyHandler as creditTransferProxyHandler
import handler.message.paymentStatusReportHandler as paymentStatusReportHandler
import handler.message.proxyHandler as proxyHandler
import handler.message.requestForPaymentHandler as requestForPaymentHandler
import handler.message.requestForPaymentRejectHandler as requestForPaymentRejectHandler
import handler.message.creditTransferRFPHandler as creditTransferRFPHandler
import handler.message.mandateRegistHandler as mandateRegistHandler
import handler.message.mandateApprovalHandler as mandateApprovalHandler
import handler.message.mandateAmendHandler as mandateAmendHandler
import os
import json
import config.serverConfig as serverConfig

import repository.data as dataDictionary

app = Flask(__name__, template_folder="templates")
app.register_blueprint(requestForPaymentBlueprint)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format/OFI')


@app.route('/getParticipantData', methods=['GET'])
def getParticipantData():
    return jsonify(dataDictionary.sampleData)


@app.route('/', methods=['GET'])
def index():
    cards = [
        {'title': 'Account Enquiry', 'content': '/AccountEnquiryOFI'},
        {'title': 'Credit Transfer', 'content': '/CreditTransferOFI'},
        {'title': 'Credit Transfer Reversal',
            'content': '/CreditTransferReversalOFI'},
        {'title': 'Credit Transfer Proxy', 'content': '/CreditTransferProxyOFI'},
        {'title': 'Payment Status', 'content': '/PaymentStatusOFI'},
        {'title': 'Proxy Registration', 'content': '/ProxyRegistrationOFI'},
        {'title': 'Proxy Porting', 'content': '/ProxyPortingOFI'},
        {'title': 'Proxy Lookup', 'content': '/ProxyLookupOFI'},
        {'title': 'Proxy Enquiry', 'content': '/ProxyEnquiryOFI'},
        {'title': 'Proxy Deactivate', 'content': '/ProxyDeactivateOFI'},
        {'title': 'Request For Pay ByAccount',
            'content': '/RequestForPayByAccountOFI'},
        {'title': 'Request For Pay ByProxy', 'content': '/RequestForPayByProxyOFI'},
        {'title': 'Request For Pay RejectByAccount',
            'content': '/RequestForPayRejectByAccountOFI'},
        {'title': 'Request For Pay RejectByProxy',
            'content': '/RequestForPayRejectByProxyOFI'},
        {'title': 'Credit Transfer RFP', 'content': '/CreditTransferRFPOFI'},
        {'title': 'Mandate Regist By Credit',
            'content': '/MandateRegistByCreditOFI'},
        {'title': 'Mandate Regist By Debit', 'content': '/MandateRegistByDebitOFI'},
        {'title': 'Mandate Approval By Credit',
            'content': '/MandateApprovalByCreditOFI'},
        {'title': 'Mandate Approval By Debit',
            'content': '/MandateApprovalByDebitOFI'},
        {'title': 'Mandate Amend By Credit', 'content': '/MandateAmendByCreditOFI'},
        {'title': 'Mandate Amend By Debit', 'content': '/MandateAmendByDebitOFI'},
        {'title': 'Mandate Amend Approval By Credit',
            'content': '/MandateAmendApprovalByCreditOFI'},
        {'title': 'Mandate Amend Approval By Debit',
            'content': '/MandateAmendApprovalByDebitOFI'},
        {'title': 'Mandate Terminate By Credit',
            'content': '/MandateTerminateByCreditOFI'},
        {'title': 'Mandate Terminate By Debit',
            'content': '/MandateTerminateByDebitOFI'},
        {'title': 'Mandate Amend By Credit', 'content': '/MandateAmendByCreditOFI'},
        {'title': 'Mandate Enquiry', 'content': '/MandateEnquiry'},
        {'title': 'Direct Debit', 'content': '/DirectDebitOFI'},
        {'title': 'Payment Status DD', 'content': '/PaymentStatusDDOFI'},
    ]
    return render_template('home.html', cards=cards)

# Account Enquiry


@app.route('/AccountEnquiryOFI', methods=['POST'])
def aeHandlerOFI():
    if request.method == 'POST':
        try:
            data = request.get_json()
            # print("Received JSON data:", data)
            response_data = {
                "status": "success",
                "message": "Request processed successfully",
            }
            # return jsonify(response_data), 200
        except Exception as e:
            pass
            # return jsonify({"error": "Invalid JSON data"}), 400
            # return jsonify({"error": f"{e}"}), 400

        # return accountEnquiryHandler.requestMessage(request.form)
        return accountEnquiryHandler.requestMessage(data)

# @app.route('/AccountEnquiryRFI', methods=['POST'])
# def aeHandlerRFI():
#     if request.method == 'POST':
#         return accountEnquiryHandler.generateResponse(request.json)

# Credit Transfer


@app.route('/CreditTransferOFI', methods=['POST'])
def ctHandlerOFI():
    if request.method == 'POST':
        return creditTransferHandler.requestMessage(request.form)

# Credit Transfer Reversal


@app.route('/CreditTransferReversalOFI', methods=['POST'])
def ctreverseHandlerOFI():
    if request.method == 'POST':
        return creditTransferReversalHandler.requestMessage(request.form)

# Credit Transfer


@app.route('/CreditTransferProxyOFI', methods=['POST'])
def ctproxyHandlerOFI():
    if request.method == 'POST':
        return creditTransferProxyHandler.requestMessage()

# PSR CT


@app.route('/PaymentStatusOFI', methods=['POST'])
def psrctHandlerOFI():
    if request.method == 'POST':
        return paymentStatusReportHandler.requestMessagePSR(request.form)

# Proxy Registration


@app.route('/ProxyRegistrationOFI', methods=['POST'])
def proxyregistHandlerOFI():
    if request.method == 'POST':
        return proxyHandler.requestMessageRegistration(request.form)

# Proxy Porting


@app.route('/ProxyPortingOFI', methods=['POST'])
def proxyportingHandlerOFI():
    if request.method == 'POST':
        return proxyHandler.requestMessagePorting(request.form)

# Proxy Lookup


@app.route('/ProxyLookupOFI', methods=['POST'])
def proxylookupHandlerOFI():
    if request.method == 'POST':
        return proxyHandler.requestMessageLookup(request.form)

# Proxy Enquiry


@app.route('/ProxyEnquiryOFI', methods=['POST'])
def proxyenquiryHandlerOFI():
    if request.method == 'POST':
        return proxyHandler.requestMessageEnquiry(request.form)

# Proxy Deactivate


@app.route('/ProxyDeactivateOFI', methods=['POST'])
def prpxydeactivateHandlerOFI():
    if request.method == 'POST':
        return proxyHandler.requestMessage(request.form)

# Request For Payment


@app.route('/RequestForPayByAccountOFI', methods=['POST'])
def rfpaccountHandlerOFI():
    if request.method == 'POST':
        return requestForPaymentHandler.requestMessageByAccount(request.form)

# Request For Payment


@app.route('/RequestForPayByProxyOFI', methods=['POST'])
def rfpproxyHandlerOFI():
    if request.method == 'POST':
        return requestForPaymentHandler.requestMessageByProxy(request.form)

# Request For Payment Rejection


@app.route('/RequestForPayRejectByAccountOFI', methods=['POST'])
def rfprejectaccountHandlerOFI():
    if request.method == 'POST':
        return requestForPaymentRejectHandler.requestMessageByAccount(request.form)

# Request For Payment Rejection


@app.route('/RequestForPayRejectByProxyOFI', methods=['POST'])
def rfprejectproxyHandlerOFI():
    if request.method == 'POST':
        return requestForPaymentRejectHandler.requestMessageByProxy(request.form)

# Credit Transfer RFP


@app.route('/CreditTransferRFPOFI', methods=['POST'])
def ctrfpHandlerOFI():
    if request.method == 'POST':
        return creditTransferRFPHandler.requestMessage(request.form)

# E-Mandate Registration by Crediting


@app.route('/MandateRegistByCreditOFI', methods=['POST'])
def mandateRegistByCreditingHandlerOFI():
    if request.method == 'POST':
        return mandateRegistHandler.requestMessageByCreditor(request.form)

# # E-Mandate Registration by Debiting
# @app.route('/MandateRegistByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# E-Mandate Approval by Crediting


@app.route('/MandateApprovalByCreditOFI', methods=['POST'])
def mandateApprovalByCreditingHandlerOFI():
    if request.method == 'POST':
        return mandateApprovalHandler.requestMessageByCreditor(request.form)

# # E-Mandate Approval by Debiting
# @app.route('/MandateApprovalByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# E-Mandate Amendment by Crediting


@app.route('/MandateAmendByCreditOFI', methods=['POST'])
def mandateAmendByCreditingHandlerOFI():
    if request.method == 'POST':
        return mandateAmendHandler.requestMessageByCreditor(request.form)

# # E-Mandate Amendment by Debiting
# @app.route('/MandateAmendByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Amendment Approval by Crediting
# @app.route('/MandateAmendApprovalByCreditOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Amendment Approval by Debiting
# @app.route('/MandateAmendApprovalByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Termination by Crediting
# @app.route('/MandateTerminateByCreditOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Termination by Debiting
# @app.route('/MandateTerminateByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Enquiry by EndToEndId
# @app.route('/MandateAmendByCreditOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# E-Mandate Enquiry by MandateID


@app.route('/MandateEnquiry', methods=['POST'])
def mandateEnquiryHandlerOFI():
    if request.method == 'POST':
        return paymentStatusReportHandler.requestMessageMandateEnquiry(request.form)

# # Direct Debit
# @app.route('/DirectDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # PSR Direct Debit
# @app.route('/PaymentStatusDDOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()


if __name__ == '__main__':
    app.run(host=serverConfig.SERVER_URL_VALUE,
            port=serverConfig.SERVER_PORT_VALUE)
