from flask import Flask, redirect, render_template, request, url_for, session

from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import _mock_collection, add_mongodata, apirequest, get_items
from portalapi.view_model import viewmodel

import os
#from dotenv import load_dotenv
#load_dotenv()

def create_app():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config())

    app.register_blueprint(blueprint, url_prefix="/login")

#    print("GitHub client ID:", os.environ.get("GITHUB_OAUTH_CLIENT_ID"))
#    print("GitHub secret:", os.environ.get("GITHUB_OAUTH_CLIENT_SECRET"))
#    print("OAuth Blueprint registered:", blueprint)
#    print(app.url_map)

    @app.route('/')
    def index():
#        global _mock_collection
#        print ("TESTING")
#        print (github)
#        if _mock_collection is None:
#            print("It is None!")
        if not github.authorized:
            print ("Not Authorised")
            return redirect(url_for("github.login"))
#        resp = github.get("/user")
#        if not resp.ok:
#            return f"GitHub API error: {resp.text}", 500
#        session['user'] = resp.json()
        items = get_items()
        item_view_model = viewmodel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-data', methods=["POST"])
    def add_data():
        add_mongodata()
        return redirect(url_for('index'))

    @app.route('/api')
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