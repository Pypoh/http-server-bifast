from flask import Blueprint

mandate_bp = Blueprint('mandate', __name__, url_prefix='/Mandate')

from . import routes  # Import the routes for this blueprint
