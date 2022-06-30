import os

from flask import Flask
from flask_migrate import Migrate

from src.db import db, init_db

migrate = Migrate()


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Load basic config. TODO: replace with remote credentials service later.
    app.config.from_pyfile(config_filename)

    # Load local overrides from config_local file
    if os.path.isfile(os.path.join('src', 'config_local.py')):
        app.config.from_pyfile('config_local.py')

    # Flask-SQLAlchemy
    init_db(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    return app
