from flask import Blueprint

payment_status_bp = Blueprint('payment_status', __name__, url_prefix='/PaymentStatus')

from . import routes  # Import the routes for this blueprint
