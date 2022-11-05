from flask import Blueprint
from flask.views import MethodView


api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@api_blueprint.route('/ping', methods=['GET'])
def ping():
    return 'PONG', 200


class ExampleAPI(MethodView):

    def get(self, sample_data=None):
        if sample_data is None:
            return 'get response', 200
        else:
            return 'Input data: {}'.format(sample_data), 200

    def post(self):
        return 'post response', 200


example_view = ExampleAPI.as_view('example')
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['GET'], defaults={'sample_data': None})
api_blueprint.add_url_rule('/example/<sample_data>', view_func=example_view, methods=['GET'])
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['POST'])
