from flask import Flask

from src.views import main, api


def register_blueprints(flask_app: Flask):
    flask_app.register_blueprint(api)
    flask_app.register_blueprint(main)
