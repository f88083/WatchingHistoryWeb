import os
import sys
from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .models import db
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        user = User.query.get(int(user_id))
        return user

    login_manager.login_view = 'main.login'

    @app.context_processor
    def inject_user():
        from .models import User
        user = User.query.first()
        return dict(user=user)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register CLI blueprint
    from .commands import app as commands_blueprint
    app.register_blueprint(commands_blueprint)

    return app

# view = Blueprint('view', __name__)

# 避免循環依賴
# from . import commands