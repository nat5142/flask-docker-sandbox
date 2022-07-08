import os

from flask import Flask
from src.blueprints import register_blueprints


def create_app(config_filename='config_local.py'):
    app = Flask(__name__)

    if os.path.isfile(os.path.join('src', config_filename)):
        app.config.from_pyfile(config_filename)

    # Register Blueprints
    register_blueprints(flask_app=app)

    return app
