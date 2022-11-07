from typing import Tuple


# JSend pattern. See here: https://github.com/omniti-labs/jsend
def api_response(status: str, data: dict = None, message: str = None, http_status_code: int = 200) -> Tuple[dict, int]:
    """ Build an API response in JSend format.

    :param status: one of ('success', 'fail', 'error')
    :type status: str
    :param data: response data, defaults to {}
    :type data: dict, optional
    :param message: error message, if error. defaults to ''
    :type message: str, optional
    :param http_status_code: HTTP status code, defaults to 200
    :type http_status_code: int, optional
    :return: (response data as dict, status code)
    :rtype: Tuple[dict, int]
    """
    ret = {'status': status, 'data': data or {}}
    if message is not None:
        ret['message'] = message
    return ret, http_status_code


def api_success(data: dict = None, http_status_code: int = 200) -> Tuple[dict, int]:
    """ Return a JSend 'success' response

    :param data: response data, defaults to None
    :type data: dict, optional
    :param http_status_code: response status code, defaults to 200
    :type http_status_code: int, optional
    :return: (response data as dict, status code)
    :rtype: Tuple[dict, int]
    """
    return api_response('success', data={} if data is None else data, http_status_code=http_status_code)


def api_fail(data: dict = None, http_status_code: int = 400) -> Tuple[dict, int]:
    """ Return a JSend 'fail' response

    :param data: response data, defaults to {}
    :type data: dict, optional
    :param http_status_code: response status code, defaults to 400
    :type http_status_code: int, optional
    :return: (response data as dict, status code)
    :rtype: Tuple[dict, int]
    """
    return api_response('fail', data={} if data is None else data, http_status_code=http_status_code)


def api_error(message: str, data: dict = None, http_status_code: int = 500) -> Tuple[dict, int]:
    """ Return a JSend 'error' response

    :param message: descriptive error message
    :type message: str
    :param data: response data, defaults to {}
    :type data: dict, optional
    :param http_status_code: response status code, defaults to 500
    :type http_status_code: int, optional
    :return: (response data as dict, status code)
    :rtype: Tuple[dict, int]
    """
    return api_response('error', data={} if data is None else data, message=message, http_status_code=http_status_code)

