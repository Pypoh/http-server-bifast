from flask import Blueprint

request_for_payment_bp = Blueprint('request_for_payment', __name__, url_prefix='/RequestForPay')

from . import routes  # Import the routes for this blueprint
