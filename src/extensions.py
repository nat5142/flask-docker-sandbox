from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


celery = Celery()
db = SQLAlchemy()
migrate = Migrate()
