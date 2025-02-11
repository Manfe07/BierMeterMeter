from flask import Blueprint
import logging

logger = logging.getLogger(__name__)

teams_Blueprint = Blueprint('teams', __name__,  template_folder='templates')

from . import routes, models