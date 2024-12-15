from flask import Blueprint

user_bp = Blueprint("users", __name__, url_prefix="/user", template_folder="templates")
from . import views
