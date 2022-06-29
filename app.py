from src.db import db
from src.main import create_app
from src.models import Users, TestTable

from flask import jsonify

# Create application in factory method
app = create_app()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/test/')
def test_table():
    query = db.session.query(TestTable)
    rows = [x.as_dict() for x in query.all()] or []

    return jsonify(rows)


@app.route('/users/')
def users():
    query = db.session.query(Users)
    rows = [x.as_dict() for x in query.all()] or []

    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
