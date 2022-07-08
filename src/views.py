from flask.blueprints import Blueprint


# plays very nicely with the app factory model. add `url_prefix=` argument for `/main/ping/` etc.
main = Blueprint('main', __name__)


@main.route('/ping/')
def ping():
    return 'PONG'


@main.route('/hello-world/')
def hello():
    return 'Hello World!'
