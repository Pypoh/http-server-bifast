from flask import Blueprint

credit_transfer_bp = Blueprint('credit_transfer', __name__, url_prefix='/CreditTransfer')

from . import routes  # Import the routes for this blueprint
