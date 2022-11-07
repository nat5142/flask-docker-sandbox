from flask import Blueprint, request
from flask.views import MethodView

from src.jsend import api_success, api_error, api_fail


api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@api_blueprint.route('/ping', methods=['GET'])
def ping():
    return 'PONG', 200


class ExampleAPI(MethodView):

    def get(self, sample_data=None):
        ret = {'path_variable': None, 'query': request.args.to_dict()}
        if sample_data is not None:
            ret['path_variable'] = sample_data

        return api_success(data=ret)

    def post(self):
        return api_success(data={'message': 'post response'})


example_view = ExampleAPI.as_view('example')
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['GET'], defaults={'sample_data': None})
api_blueprint.add_url_rule('/example/<sample_data>', view_func=example_view, methods=['GET'])
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['POST'])
