import os
import time

from celery.schedules import crontab
from flask import Flask

from src.db import db, init_db
from src.extensions import celery, migrate


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

    # Celery
    make_celery(app)

    return app


def make_celery(app=None):
    """ Create and return Celery instance. More info: https://flask.palletsprojects.com/en/2.1.x/patterns/celery/ """
    app = app or create_app()
    celery.conf.update(app.config.get('CELERY_CONFIG', {}))
    celery.conf.timezone = os.environ.get('CELERY_TIMEZONE', 'UTC')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # Register periodic tasks
    register_tasks(celery)

    return celery


def register_tasks(celery_app):
    celery_app.conf.beat_schedule = {
        'example-task': {
            'task': 'logging_task',
            'schedule': crontab(minute='*/2'),
            'args': (time.time())
        }
    }
