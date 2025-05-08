from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from mongomock import ObjectId

from portalapi.data.trello_data import add_trellodata
from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from flask import current_app
from flask import has_request_context, request
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import _mock_collection, add_mongodata, apirequest, get_items, get_post_collection
from portalapi.view_model import viewmodel
from loggly.handlers import HTTPSHandler
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

from functools import wraps

import os

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.path = request.path
        else:
            record.url = record.remote_addr = record.method = record.path = "-"
        return super().format(record)
    
def configure_logging(app):
    log_level = app.config.get("LOGS_LEVEL", logging.INFO)

    # Clear existing handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    app.logger.setLevel(log_level)
    formatter = RequestFormatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s '
        '[%(method)s %(path)s from %(remote_addr)s]'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # File Handler (rotating)
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Loggly Handler
    token = app.config.get("LOGGLY_TOKEN")
    if token:
        loggly_handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{token}/tag/portalapiapp')
        loggly_handler.setFormatter(formatter)
        loggly_handler.setLevel(log_level)
        app.logger.addHandler(loggly_handler)
        app.logger.info("Loggly logging is enabled.")

    # Final log to confirm
    app.logger.propagate = False
    app.logger.info('Logging has been fully configured.')


def github_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            print("Not Authorised")
            current_app.logger.info("Login Failure - Unauthorised.")
            return redirect(url_for("github.login"))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config())

#    app.logger.setLevel(app.config['LOGS_LEVEL'])
#    app.logger.info("Log Level - %s", app.config['LOGS_LEVEL'])
#    app.logger.info("Loggly token - %s", app.config['LOGGLY_TOKEN'])

    configure_logging(app)

    @app.before_request
    def log_request_info():
        current_app.logger.info("Incoming request")
#        current_app.logger.info(
#            f"Incoming request: {request.method} {request.path} from {request.remote_addr}"
#        )

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/portalapiapp')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)
        app.logger.info("Logged in User - %s", os.getlogin())

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled exception occurred:")
        return render_template("error.html", message="An unexpected error occurred."), 500

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


    @app.route('/hpa')
    def hpa_loading():
        sum(i*i for i in range(10000000))
        return redirect(url_for("index"))
    
    return app