from flask import current_app, jsonify, render_template, redirect, flash, url_for, request, abort
from flask.blueprints import Blueprint
from flask_login import login_user, current_user
from urllib.parse import urlparse, urljoin

from src.db import db
from src.forms import LoginForm, RegisterForm
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
        
        return redirect(url_for('main.ping'))
    
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
            flash('Success!')
        return redirect(url_for('main.login'))  # always return to login screen after invalid submit
    
    return render_template('register.html', title='Register', form=form)


# TODO: Implement password reset
    


def is_safe_url(target):
    current_app.logger.warning('Login redirect URL target: {}'.format(target))

    if not target:
        return True

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return ref_url.netloc == test_url.netloc
