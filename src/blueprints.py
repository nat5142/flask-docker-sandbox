from flask import Flask

from src.views import api_blueprint


def register_blueprints(flask_app: Flask):
    flask_app.register_blueprint(api_blueprint)