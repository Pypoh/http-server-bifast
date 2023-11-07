from flask import Blueprint

bulk_bp = Blueprint(
    'bulk', __name__, url_prefix='/Bulk')

from . import routes