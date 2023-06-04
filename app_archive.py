import sys
from blueprints.RequestForPayment import requestForPaymentBlueprint
from flask import Flask, render_template, request, Blueprint, jsonify, Response
import handler.general as handler
import handler.message.accountEnquiryHandler as accountEnquiryHandler
from datetime import datetime
import pytz
import json
import os
from collections import OrderedDict


app = Flask(__name__)
app.register_blueprint(requestForPaymentBlueprint)
app.config['FORMAT_PATH'] = os.path.join(app.root_path, 'format')


@app.route('/')
def home():
    return render_template('test.html')


@app.route('/test', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        print('Hello world!', file=sys.stderr)
        return "{'Hasil RFI'}"
        # return render_template('test.html')

@app.route('/AEtest', methods=['GET', 'POST'])
def aeHandler():
    if request.method == 'POST':
        return accountEnquiryHandler.generateResponse(request.json)


@app.route('/messageTest', methods=['GE T', 'POST'])
def messageTest():
    if request.method == 'POST':
        filePath = os.path.join(app.root_path, 'format', 'pacs.002.json')
        with open(filePath, 'r') as jsonTemplate:
            templateData = json.load(jsonTemplate)
            # templateData = json.load(jsonTemplate, object_pairs_hook=OrderedDict)
            bizMsgIdr = handler.generateBizMsgIdr("821")
            wibTimeZone = pytz.timezone('Asia/Jakarta')
            currentTime = datetime.now(wibTimeZone)
            formattedTimestamp = currentTime.strftime('%Y-%m-%dT%H:%M:%SZ')
            return str(templateData)

            # data = OrderedDict()
            # data['BusMsg'] = OrderedDict()
            # data['BusMsg']['AppHdr'] = OrderedDict()
            # data['BusMsg']['AppHdr']['Fr'] = OrderedDict()
            # data['BusMsg']['AppHdr']['Fr']['FIId'] = OrderedDict()
            # data['BusMsg']['AppHdr']['Fr']['FIId']['FinInstnId'] = OrderedDict()
            # data['BusMsg']['AppHdr']['Fr']['FIId']['FinInstnId']['Othr'] = OrderedDict()
            # data['BusMsg']['AppHdr']['Fr']['FIId']['FinInstnId']['Othr']['Id'] = "ARTGIDJA"
            # data['BusMsg']['AppHdr']['To']['FIId']['FinInstnId']['Othr']['Id'] = "FASTIDJA"
            # data['BusMsg']['AppHdr']['BizMsgIdr'] = bizMsgIdr
            # data.update(templateData)

            # return jsonify(templateData)

        # json_data = request.get_json()
        # # bizMsgIdr = json_data.get('BizMsgIdr')
        # bizMsgIdr = handler.generateBizMsgIdr("821")

        # wibTimezone = pytz.timezone('Asia/Jakarta')
        # currentTime = datetime.now(wibTimezone)
        # formattedTimestamp = currentTime.strftime('%Y-%m-%dT%H:%M:%SZ')

        # template_args = {
        #     'name': name,
        #     'age': age,
        #     'city': city
        # }

        # response = {'BizMsgIdr': f'{bizMsgIdr}',
        #             'CreDt': f'{formattedTimestamp}'}
        # return jsonify(response), 200


@app.route('/testJson', methods=['GET', 'POST'])
def testJson():
    if request.method == 'POST':
        filePath = os.path.join(app.root_path, 'format', 'pacs.002.json')
            # bizMsgIdr = handler.generateBizMsgIdr("821")
            # wibTimeZone = pytz.timezone('Asia/Jakarta')
            # currentTime = datetime.now(wibTimeZone)
            # formattedTimestamp = currentTime.strftime('%Y-%m-%dT%H:%M:%SZ')
        with open(filePath, 'r') as file:
            template_data = json.load(file)
            value_dict = {
                "FrBIC": "ARTGIDJA",
                "ToBIC": "TO_BIC_VALUE",
                "BizMsgIdr": "BIZ_MSG_IDR_VALUE",
                "CreDt": "CRE_DT_VALUE",
            }
        filled_data = handler.replace_placeholders(template_data, value_dict)
        json_data = json.dumps(filled_data, indent=0)
        response = Response(json_data, content_type='application/json')
        return response


if __name__ == '__main__':
    # app.run(host='10.199.13.67', port='18907')
    app.run()
