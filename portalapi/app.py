from flask import Flask, redirect, render_template, request, url_for, session

from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import _mock_collection, add_mongodata, apirequest, get_items
from portalapi.view_model import viewmodel

from functools import wraps

import os

def github_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            print("Not Authorised")
            return redirect(url_for("github.login"))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config())

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    @github_login_required
    def index():
        items = get_items()
        item_view_model = viewmodel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-data', methods=["POST"])
    @github_login_required
    def add_data():
        add_mongodata()
        return redirect(url_for('index'))

    @app.route('/api')
    @github_login_required
    def api_request():
        customer = request.args.get('customer', default='*', type=str)
        salesorder = request.args.get('salesorder', default='*', type=str)
        engineer = request.args.get('engineer', default='*', type=str)
        apirequest(customer, salesorder, engineer)
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect(url_for('index'))

    return app