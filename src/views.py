from flask import Blueprint, request, current_app, jsonify, render_template, redirect, flash, url_for, abort
from flask.views import MethodView
from flask.blueprints import Blueprint
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from urllib.parse import urlparse, urljoin

from src.db import db
from src.forms import LoginForm, RegisterForm, TriggerPasswordResetForm, PasswordResetForm
from src.jsend import api_success, api_error, api_fail
from src.mail import send_email
from src.models import Users, TestTable
from src.tokens import generate_token, confirm_token


# plays very nicely with the app factory model. add `url_prefix=` argument for `/main/ping/` etc.
main = Blueprint('main', __name__)
api = Blueprint('api', __name__, url_prefix='/api/v1')


@main.route('/')
def index():
    return redirect(url_for('main.hello'))


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
@login_required
def users():
    query = db.session.query(Users)
    rows = [x.as_dict() for x in query.all()] or []

    return jsonify(rows)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Only get here from valid POSTs
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            current_app.logger.warning('User not found: {}'.format(form.email.data))
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not is_safe_url(next_page):
            return abort(400)
        
        return redirect(url_for('main.hello'))
    
    return render_template('login.html', title='Log In', form=form)


@main.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.ping'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash('This email address is already registered for an account.')
        else:
            user = Users(email=form.email.data, username=form.username.data)
            user.set_password(form.password.data)
            user.save()

            token = generate_token(user.email, salt_key='SECURITY_PASSWORD_SALT')
            confirm_url = url_for('main.confirm_email_verify_token', token=token, _external=True)
            html = render_template('email/verify.html', confirm_url=confirm_url)
            subject = 'Please confirm your email for flask-docker-sandbox'
            
            message = Message(
                subject=subject,
                recipients=[user.email],
                sender=('flask-docker-sandbox', 'noreply@flask-docker-sandbox.com'),
                html=html
            )

            send_email(message)

            return redirect(url_for('main.verify_email'))
    
    return render_template('register.html', title='Register', form=form)


@main.route('/verify-email/', methods=['GET', 'POST'])
def verify_email():
    return render_template('verify_email.html')


@main.route('/confirm/<token>', methods=['GET'])
def confirm_email_verify_token(token):
    try:
        email = confirm_token(token, salt_key='SECURITY_PASSWORD_SALT')
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        abort(404)
    else:
        user = Users.query.filter_by(email=email).first_or_404()
        if user.email_verified:
            flash('Account already confirmed. Please log in.', 'success')
        else:
            user.email_verified = True
            user.save()
            return render_template('email_verified.html')

        return redirect(url_for('main.login'))          


@main.route('/send-reset-password-email/', methods=['GET', 'POST'])
def password_reset_email():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = TriggerPasswordResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_token(user.email, 'PASSWORD_RESET_SALT')
            reset_password_url = url_for('main.reset_password', token=token, _external=True)
            html = render_template('email/reset_password_email.html', reset_password_url=reset_password_url)
            subject = 'Reset your flask-docker-sandbox password.'

            msg = Message(
                subject=subject,
                recipients=[user.email],
                sender=('flask-docker-sandbox', 'noreply@flask-docker-sandbox.com'),
                html=html
            )

            send_email(msg)

            flash('Check your email inbox for instructions to reset your password.')
            return redirect(url_for('main.login'))
        else:
            flash('We don\'t have an account with this email.')
    
    return render_template('request_password_reset.html', title='Reset Password', form=form)
    

@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = confirm_token(token, salt_key='PASSWORD_RESET_SALT')
    except:
        flash('This password reset link is invalid or has expired.', 'danger')
        abort(404)
    else:
        form = PasswordResetForm()
        if form.validate_on_submit():
            if email != form.email.data:
                flash('Who are you?')
                abort(403)
            user = Users.query.filter_by(email=email).first_or_404()
            user.set_password(form.password.data)
            user.save()
            if user.email_verified:
                flash('Password successfully reset.', 'success')
                return render_template('password_reset_success.html')
            else:
                flash('Your email is still unverified. Fix that.', 'danger')
                return redirect(url_for('main.verify_email'))

        return render_template('reset_password.html', form=form)


@main.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


def is_safe_url(target):
    current_app.logger.warning('Login redirect URL target: {}'.format(target))

    if not target:
        return True

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return ref_url.netloc == test_url.netloc


##############
# API Routes #
##############

@api.route('/ping', methods=['GET'])
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
api.add_url_rule('/example', view_func=example_view, methods=['GET'], defaults={'sample_data': None})
api.add_url_rule('/example/<sample_data>', view_func=example_view, methods=['GET'])
api.add_url_rule('/example', view_func=example_view, methods=['POST'])
