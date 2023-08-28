from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def generate_token(email, salt_key):
    """ Generate a token. Will throw a KeyError if salt_key is not defined in config.
    :param email: email address to generate a token for
    :param salt_key: retrieve salt key from config using this value
    :return: string
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config[salt_key])


def confirm_token(token, salt_key, expiration=3600):
    """ Confirm an email registration token.
    :param token:
    :param salt_key: retrieve salt key from config using this value
    :param expiration: expiration time, in seconds. defaults to 1 hour
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config[salt_key],
            max_age=expiration
        )
    except Exception as exc:
        return False

    return email


