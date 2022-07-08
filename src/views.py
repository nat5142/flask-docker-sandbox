from flask import jsonify
from flask.blueprints import Blueprint

from src.db import db
from src.models import Users, TestTable


# plays very nicely with the app factory model. add `url_prefix=` argument for `/main/ping/` etc.
main = Blueprint('main', __name__)


@main.route('/ping/')
def ping():
    return 'PONG'


@main.route('/hello-world/')
def hello():
    return 'Hello World!'


@main.route('/test/')
def test_table():
    query = db.session.query(TestTable)
    rows = [x.as_dict() for x in query.all()] or []

    return jsonify(rows)


@main.route('/users/')
def users():
    query = db.session.query(Users)
    rows = [x.as_dict() for x in query.all()] or []

    return jsonify(rows)
