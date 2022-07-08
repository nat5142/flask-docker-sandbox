from src.views import main


def register_blueprints(flask_app):
    flask_app.register_blueprint(main)
