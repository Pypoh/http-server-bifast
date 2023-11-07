from flask import Blueprint

credit_transfer_bp = Blueprint('response', __name__, url_prefix='/Response')

from . import routes  # Import the routes for this blueprint
