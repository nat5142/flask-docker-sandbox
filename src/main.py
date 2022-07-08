from cmath import log
from distutils.log import Log
import os

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from src.db import db, init_db
from src.models.user import User

migrate = Migrate()


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Load basic config. TODO: replace with remote credentials service later.
    app.config.from_pyfile(config_filename)

    # Load local overrides from config_local file
    if os.path.isfile(os.path.join('src', 'config_local.py')):
        app.config.from_pyfile('config_local.py')

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Flask-SQLAlchemy
    init_db(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    return app
