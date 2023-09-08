# from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, request, render_template, jsonify
from config import serverConfig
# from handler import general as handler
# import handler.general as handler
from blueprints.account_enquiry import account_enquiry_bp
from blueprints.credit_transfer import credit_transfer_bp
from blueprints.request_for_payment import request_for_payment_bp
from blueprints.mandate import mandate_bp
from blueprints.payment_status import payment_status_bp
from blueprints.direct_debit import direct_debit_bp
from repository import data as dataDictionary
import os
import json
import requests

app = Flask(__name__, template_folder="templates")
app.register_blueprint(account_enquiry_bp)
app.register_blueprint(credit_transfer_bp)
app.register_blueprint(request_for_payment_bp)
app.register_blueprint(mandate_bp)
app.register_blueprint(payment_status_bp)
app.register_blueprint(direct_debit_bp)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format/OFI')


@app.route('/getParticipantData', methods=['GET'])
def getParticipantData():
    return jsonify(dataDictionary.sampleData)


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', cards=dataDictionary.cards)

# HTML Template
@app.route('/sanity', methods=['GET'])
def sanity():
    return render_template('sanity.html', cards=dataDictionary.cards)

# HTML Template
@app.route('/simulator', methods=['GET'])
def simulator():
    return render_template('simulator.html', cards=dataDictionary.cards)

# HTML Template
@app.route('/setting', methods=['GET'])
def setting():
    return render_template('setting.html', data=dataDictionary.sampleData)






# @app.route('/AccountEnquiryRFI', methods=['POST'])
# def aeHandlerRFI():
#     if request.method == 'POST':
#         return accountEnquiryHandler.generateResponse(request.json)



# # Credit Transfer
# @app.route('/CreditTransferOFI', methods=['POST'])
# def ctHandlerOFI():
#     if request.method == 'POST':

#         # TODO: save to db

#         return creditTransferHandler.requestMessage()

# # Credit Transfer Reversal
# @app.route('/CreditTransferReversalOFI', methods=['POST'])
# def ctreverseHandlerOFI():
#     if request.method == 'POST':
#         # ct_response = requests.post(
#         #     f'http://{serverConfig.SERVER_URL_VALUE}:{serverConfig.SERVER_PORT_VALUE}/CreditTransferOFI')

#         data = request.get_json()

#         return creditTransferReversalHandler.requestMessage(data)

# # Credit Transfer
# @app.route('/CreditTransferProxyOFI', methods=['POST'])
# def ctproxyHandlerOFI():
#     if request.method == 'POST':
#         return creditTransferProxyHandler.requestMessage()

# # PSR CT
# @app.route('/PaymentStatusOFI', methods=['POST'])
# def psrctHandlerOFI():
#     if request.method == 'POST':
#         return paymentStatusReportHandler.requestMessagePSR(request.form)

# # Proxy Registration
# @app.route('/ProxyRegistrationOFI', methods=['POST'])
# def proxyregistHandlerOFI():
#     if request.method == 'POST':
#         return proxyHandler.requestMessageRegistration(request.form)

# # Proxy Porting
# @app.route('/ProxyPortingOFI', methods=['POST'])
# def proxyportingHandlerOFI():
#     if request.method == 'POST':
#         return proxyHandler.requestMessagePorting(request.form)

# # Proxy Lookup
# @app.route('/ProxyLookupOFI', methods=['POST'])
# def proxylookupHandlerOFI():
#     if request.method == 'POST':
#         return proxyHandler.requestMessageLookup(request.form)

# # Proxy Enquiry
# @app.route('/ProxyEnquiryOFI', methods=['POST'])
# def proxyenquiryHandlerOFI():
#     if request.method == 'POST':
#         return proxyHandler.requestMessageEnquiry(request.form)

# # Proxy Deactivate
# @app.route('/ProxyDeactivateOFI', methods=['POST'])
# def prpxydeactivateHandlerOFI():
#     if request.method == 'POST':
#         return proxyHandler.requestMessage(request.form)

# # Request For Payment
# @app.route('/RequestForPayByAccountOFI', methods=['POST'])
# def rfpaccountHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()

# # Request For Payment
# @app.route('/RequestForPayByProxyOFI', methods=['POST'])
# def rfpproxyHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage(True)

# # Request For Payment Rejection
# @app.route('/RequestForPayRejectByAccountOFI', methods=['POST'])
# def rfprejectaccountHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentRejectHandler.requestMessageByAccount(request.form)

# # Request For Payment Rejection
# @app.route('/RequestForPayRejectByProxyOFI', methods=['POST'])
# def rfprejectproxyHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentRejectHandler.requestMessageByProxy(request.form)

# # Credit Transfer RFP
# @app.route('/CreditTransferRFPOFI', methods=['POST'])
# def ctrfpHandlerOFI():
#     if request.method == 'POST':
#         return creditTransferRFPHandler.requestMessage(request.form)

# # E-Mandate Registration by Crediting
# @app.route('/MandateRegistByCreditOFI', methods=['POST'])
# def mandateRegistByCreditingHandlerOFI():
#     if request.method == 'POST':
#         # return mandateRegistHandler.requestMessageByCreditor(request.form)
#         # return mandateRegistHandler.requestMessage(request.form)
#         return mandateRegistHandler.requestMessageXml(request.form)

# # # E-Mandate Registration by Debiting
# # @app.route('/MandateRegistByDebitOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # E-Mandate Approval by Crediting
# @app.route('/MandateApprovalByCreditOFI', methods=['POST'])
# def mandateApprovalByCreditingHandlerOFI():
#     if request.method == 'POST':
#         return mandateApprovalHandler.requestMessage(request.form)
#         # return mandateApprovalHandler.requestMessageByCreditor(request.form)

# # # E-Mandate Approval by Debiting
# # @app.route('/MandateApprovalByDebitOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # E-Mandate Amendment by Crediting
# @app.route('/MandateAmendByCreditOFI', methods=['POST'])
# def mandateAmendByCreditingHandlerOFI():
#     if request.method == 'POST':
#         return mandateAmendHandler.requestMessage(request.form)
#         # return mandateAmendHandler.requestMessageByCreditor(request.form)

# # # E-Mandate Amendment by Debiting
# # @app.route('/MandateAmendByDebitOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # # E-Mandate Amendment Approval by Crediting
# # @app.route('/MandateAmendApprovalByCreditOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # # E-Mandate Amendment Approval by Debiting
# # @app.route('/MandateAmendApprovalByDebitOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # # E-Mandate Termination by Crediting
# # @app.route('/MandateTerminateByCreditOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # # E-Mandate Termination by Debiting
# # @app.route('/MandateTerminateByDebitOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # # E-Mandate Enquiry by EndToEndId
# # @app.route('/MandateAmendByCreditOFI', methods=['POST'])
# # def rfpHandlerOFI():
# #     if request.method == 'POST':
# #         return requestForPaymentHandler.requestMessage()

# # E-Mandate Enquiry by MandateID
# @app.route('/MandateEnquiry', methods=['POST'])
# def mandateEnquiryHandlerOFI():
#     if request.method == 'POST':
#         return paymentStatusReportHandler.requestMessageMandateEnquiry(request.form)

# # Direct Debit
# @app.route('/DirectDebitOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return directDebitHandler.requestMessage(request.form)

# # PSR Direct Debit
# @app.route('/PaymentStatusDDOFI', methods=['POST'])
# def rfpHandlerOFI():
#     if request.method == 'POST':
#         return requestForPaymentHandler.requestMessage()


if __name__ == '__main__':
    app.run(host=serverConfig.SERVER_URL_VALUE,
            port=serverConfig.SERVER_PORT_VALUE)
