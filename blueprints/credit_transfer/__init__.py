from flask import Blueprint

account_enquiry_bp = Blueprint('account_enquiry', __name__, url_prefix='/AccountEnquiry')

from . import routes  # Import the routes for this blueprint
