from flask import Blueprint, request, current_app
from flask.views import MethodView

from src.jsend import api_success, api_error, api_fail


api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')


@api_blueprint.route('/ping', methods=['GET'])
def ping():
    return 'PONG', 200


class ExampleAPI(MethodView):

    def get(self, sample_data=None):
        try:
            ret = {'path_variable': None, 'query': request.args.to_dict()}
            if sample_data is not None:
                ret['path_variable'] = sample_data

            return api_success(data=ret)
        except Exception as exc:
            return api_error(exc.args[0])

    def post(self):
        try:
            try:
                request_json = request.get_json(force=True)
            except Exception as exc:
                current_app.logger.debug(exc)
                return api_fail(data={'messages': 'Error parsing request body.'})
            else:
                if not request_json:
                    return api_fail(data={'messages': 'Please send request body as JSON.'})
                else:
                    return api_success(data={'request': {'body': request.get_json(force=True)}})
        except Exception as exc:
            return api_error(exc.args[0])


example_view = ExampleAPI.as_view('example')
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['GET'], defaults={'sample_data': None})
api_blueprint.add_url_rule('/example/<sample_data>', view_func=example_view, methods=['GET'])
api_blueprint.add_url_rule('/example', view_func=example_view, methods=['POST'])
