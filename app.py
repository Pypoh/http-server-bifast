from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, request
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
import os
import config.serverConfig as serverConfig

app = Flask(__name__)
app.register_blueprint(requestForPaymentBlueprint)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format/OFI')

# @app.route('/', methods=['POST'])
# def rfpHandlerRFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.generateResponse(request.json)

# Account Enquiry
@app.route('/AccountEnquiryOFI', methods=['POST'])
def aeHandlerOFI():
    if request.method == 'POST':
        return accountEnquiryHandler.requestMessage(request.form)

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
        return paymentStatusReportHandler.requestMessage(request.form)

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

# # E-Mandate Approval by Crediting
# @app.route('/MandateApprovalByCreditOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Approval by Debiting
# @app.route('/MandateApprovalByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # E-Mandate Amendment by Crediting
# @app.route('/MandateAmendByCreditOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

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

# # E-Mandate Enquiry by MandateID
# @app.route('/MandateAmendByDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

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
    app.run(host=serverConfig.SERVER_URL_VALUE, port=serverConfig.SERVER_PORT_VALUE)
