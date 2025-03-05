from flask import Blueprint
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/static/main',)


from . import routes
