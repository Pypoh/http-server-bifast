from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, request
import handler.general as handler
import handler.message.accountEnquiryHandler as accountEnquiryHandler
import os

app = Flask(__name__)
app.register_blueprint(requestForPaymentBlueprint)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format')


# OFI Account Enquiry
# RFI Account Enquiry
@app.route('/AccountEnquiryOFI', methods=['POST'])
def aeHandler():
    if request.method == 'POST':
        return accountEnquiryHandler.generateResponse(request.json)

# RFI Account Enquiry
@app.route('/AccountEnquiryRFI', methods=['POST'])
def aeHandler():
    if request.method == 'POST':
        return accountEnquiryHandler.generateResponse(request.json)


if __name__ == '__main__':
    # app.run(host='10.199.13.67', port='18907')
    app.run()
