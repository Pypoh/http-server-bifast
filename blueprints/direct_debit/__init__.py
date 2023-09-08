from flask import Blueprint

direct_debit_bp = Blueprint('direct_debit', __name__, url_prefix='/DirectDebit')

from . import routes  # Import the routes for this blueprint
