from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, request
import handler.general as handler
import handler.message.accountEnquiryHandler as accountEnquiryHandler
import handler.message.requestForPaymentHandler as requestForPaymentHandler
import os
import config.serverConfig as serverConfig

app = Flask(__name__)
app.register_blueprint(requestForPaymentBlueprint)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format')

@app.route('/', methods=['POST'])
def rfpHandlerRFI():
    if request.method == 'POST':
        return requestForPaymentHandler.generateResponse(request.json)

@app.route('/AccountEnquiryOFI', methods=['POST'])
def aeHandlerOFI():
    if request.method == 'POST':
        return accountEnquiryHandler.requestMessage()

@app.route('/AccountEnquiryRFI', methods=['POST'])
def aeHandlerRFI():
    if request.method == 'POST':
        return accountEnquiryHandler.generateResponse(request.json)

if __name__ == '__main__':
    app.run(host=serverConfig.SERVER_URL_VALUE, port=serverConfig.SERVER_PORT_VALUE)
