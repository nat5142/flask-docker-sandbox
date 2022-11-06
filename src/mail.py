from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


def send_email(msg: Message):
    try:
        mail.send(msg)
    except Exception as exc:
        current_app.logger.error(exc)
        raise
