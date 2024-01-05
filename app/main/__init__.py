from flask import Blueprint

# Main blueprint
main = Blueprint('main', __name__)

# 避免循環依賴
from . import views, errors

# from main.views import view as view_blueprint
# app.register_blueprint(view_blueprint)