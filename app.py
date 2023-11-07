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
from blueprints.bulk import bulk_bp
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
app.register_blueprint(bulk_bp)
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

# HTML Template


@app.route('/proxy', methods=['GET'])
def proxy():
    return render_template('proxy.html', data=dataDictionary.sampleData)

# HTML Template


@app.route('/bulk', methods=['GET'])
def bulk():
    return render_template('bulk.html', bulk_data=dataDictionary.bulk_data)


if __name__ == '__main__':
    app.run(host=serverConfig.SERVER_URL_VALUE,
            port=serverConfig.SERVER_PORT_VALUE)
