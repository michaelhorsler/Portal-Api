from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from mongomock import ObjectId

from portalapi.data.trello_data import add_trellodata
from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import _mock_collection, add_mongodata, apirequest, get_items, get_post_collection
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
        try:
            items = get_items()
            item_view_model = viewmodel(items)
        except Exception as e:
            # Handle the MongoDB connection failure
            return render_template('error.html', message="MongoDB connection failed: " + str(e)), 500

        user = None
        if github.authorized:
            resp = github.get("/user")
            if resp.ok:
                user = resp.json()

    # Add logic to pass a message if no items are found
        message = None
        if not items:  # Check if the items list is empty
            message = "No posts available"

        return render_template('index.html', view_model=item_view_model, user=user, message=message)

   #     return render_template('index.html', view_model=item_view_model, user=user)

    @app.route('/add-data', methods=["POST"])
    @github_login_required
    def add_data():
  #      add_mongodata()
        add_trellodata()
        return redirect(url_for('index'))

    @app.route('/api')
    @github_login_required
    def api_request():
        customer = request.args.get('customer', default='*', type=str)
        salesorder = request.args.get('salesorder', default='*', type=str)
        engineer = request.args.get('engineer', default='*', type=str)
        apirequest(customer, salesorder, engineer)
        add_trellodata(customer, salesorder, engineer)
        return redirect(url_for('index'))
    
    @app.route('/posts/<post_id>', methods=['DELETE'])
    def delete_post(post_id):
        try:
            posts = get_post_collection()
            result = posts.delete_one({"_id": ObjectId(post_id)})
            if result.deleted_count == 0:
                return jsonify({"message": "Post not found"}), 404
            return jsonify({"message": "Post deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    
    @app.route('/login')
    @github_login_required
    def login():
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        token = github.blueprint.token["access_token"]
        del github.blueprint.token  # clear session
        print(f"User logged out: {token}")
        return redirect(url_for("index"))

    return app