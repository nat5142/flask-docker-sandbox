import os

from flask import Flask
from flask_migrate import Migrate

from src.db import db, init_db

migrate = Migrate()


def create_app(config_filename='config_local.py'):
    app = Flask(__name__)

    if os.path.isfile(os.path.join('src', config_filename)):
        # Load local config file
        app.config.from_pyfile(config_filename)

    # Flask-SQLAlchemy
    init_db(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    return app
