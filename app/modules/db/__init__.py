from flask import Blueprint

db = Blueprint('db', __name__, url_prefix="/db", template_folder="templates")

from . import routes
