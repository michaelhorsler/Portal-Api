from flask import Flask, redirect, render_template, request, url_for, session

from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import add_mongodata, apirequest, get_items
from portalapi.view_model import viewmodel

import os

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    def index():
        if not github.authorized:
            return redirect(url_for("github.login"))
        resp = github.get("/user")
        assert resp.ok, resp.text
        session['user'] = resp.json()
        items = get_items()
        item_view_model = viewmodel(items)
        return render_template('index.html', view_model=item_view_model, user=session['user'])

    @app.route('/add-data', methods=["POST"])
    def add_data():
        add_mongodata()
        return redirect('/')

    @app.route('/api')
    def api_request():
        customer = request.args.get('customer', default='*', type=str)
        salesorder = request.args.get('salesorder', default='*', type=str)
        engineer = request.args.get('engineer', default='*', type=str)
        apirequest(customer, salesorder, engineer)
        return redirect('/')

    return app