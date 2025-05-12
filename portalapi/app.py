from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from mongomock import ObjectId
import requests
import getpass
import json
from datetime import datetime

from portalapi.data.trello_data import add_trellodata
from portalapi.flask_config import Config
from portalapi.oauth import blueprint
from flask_dance.contrib.github import github
from flask import current_app
from flask import has_request_context, request
from flask import send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from portalapi.data.mongo_data import _mock_collection, add_mongodata, apirequest, get_items, get_post_collection
from portalapi.view_model import viewmodel
from loggly.handlers import HTTPSHandler
import logging
import atexit
from logging.handlers import RotatingFileHandler, SMTPHandler
from logging import Formatter

from functools import wraps

import os

class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.path = request.path
        else:
            record.url = record.remote_addr = record.method = record.path = "-"
        return super().format(record)
    
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "status": getattr(record, "status", None),
            "component": getattr(record, "component", "portalapi"),
            "path": getattr(record, "pathname", None),
            "function": getattr(record, "funcName", None),
        }

        if has_request_context():
            log_record.update({
                "url": request.url,
                "remote_addr": request.remote_addr,
                "method": request.method,
                "route": request.path,
            })
        else:
            log_record.update({
                "url": "-",
                "remote_addr": "-",
                "method": "-",
                "route": "-",
            })

        return json.dumps(log_record)
    
class SlackHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        try:
            log_entry = self.format(record)
            requests.post(self.webhook_url, json={"text": log_entry})
        except Exception:
            self.handleError(record)

def configure_logging(app):
    level_name = app.config.get("LOGS_LEVEL", "INFO").upper()
    log_level = getattr(logging, level_name, logging.INFO)
    # Clear existing handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    app.logger.setLevel(log_level)
    formatter = JSONFormatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s '
        '[%(method)s %(path)s from %(remote_addr)s]'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # Loggly Handler
    token = app.config.get("LOGGLY_TOKEN")
    if token:
        loggly_handler = HTTPSHandler(url=f'https://logs-01.loggly.com/inputs/{token}/tag/portalapi')
        loggly_handler.setFormatter(formatter)
        loggly_handler.setLevel(log_level)
        app.logger.addHandler(loggly_handler)
        app.logger.info(
            "Loggly logging is enabled.",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("Loggly logging is enabled.")
    else:
        print("No Loggly token found. Skipping Loggly handler setup.")

    # File Handler (rotating)
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Error File
    error_file_handler = RotatingFileHandler('error.log', maxBytes=10240, backupCount=3)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
    app.logger.info(
        "Error file logging is enabled.",
        extra={"status": "RECOVERY", "component": "portalapi"}
    )
#    app.logger.info("Error file logging is enabled.")

    # Email for critical errors
    if app.config.get("MAIL_SERVER"):
        auth = None
        print("here")
        if app.config.get("MAIL_USERNAME") and app.config.get("MAIL_PASSWORD"):
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secure = () if app.config.get("MAIL_USE_TLS") else None

        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr=app.config["MAIL_DEFAULT_SENDER"],
            toaddrs=app.config["MAIL_ADMINS"],
            subject="🚨 Flask Application Error",
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)
        app.logger.info(
            "Email error handler attached.",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("Email error handler attached.")

    # Slack for critical errors
    webhook = app.config.get("SLACK_WEBHOOK_URL")
    if webhook:
        slack_handler = SlackHandler(webhook)
        slack_handler.setLevel(logging.ERROR)
        slack_handler.setFormatter(formatter)
        app.logger.addHandler(slack_handler)
        app.logger.info(
            "Slack error handler attached.",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("Slack error handler attached.")

    # Final log to confirm
    app.logger.propagate = False
    app.logger.info(
        "Logging has been fully configured.",
        extra={"status": "RECOVERY", "component": "portalapi"}
    )
#    app.logger.info('Logging has been fully configured.')

    # Ensure handler is flushed and closed at shutdown
    def shutdown_logging():
        handlers = app.logger.handlers[:]
        for handler in handlers:
            handler.flush()
            handler.close()
            app.logger.removeHandler(handler)

    atexit.register(shutdown_logging)

def github_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not github.authorized:
            print("Not Authorised")
            current_app.logger.info(
                "Login Failure - Unauthorised.",
                extra={"status": "RECOVERY", "component": "portalapi"}
            )
#            current_app.logger.info("Login Failure - Unauthorised.")
            return redirect(url_for("github.login"))
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.config.from_object(Config())

    configure_logging(app)

    @app.before_request
    def log_request_info():
        if request.path.startswith('/static/') or request.path.endswith(('.png', '.jpg', '.jpeg', '.ico', '.gif', '.css', '.js')):
            return  # Skip logging static/image requests
        current_app.logger.info(
            "Incoming request",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        current_app.logger.info("Incoming request")

    if not os.getenv("PYTEST_CURRENT_TEST"):
        try:
            user = getpass.getuser()
        except Exception:
            user = "unknown"
        app.logger.info(
            f"Logged in User - {user}",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("Logged in User - %s", user)
    app.register_blueprint(blueprint, url_prefix="/login")

    @app.errorhandler(Exception)
    def handle_exception(e):
#        app.logger.exception("Unhandled exception occurred:")
        app.logger.error(
            "Unhandled exception occurred.",
            extra={"status": "FAILURE", "component": "portalapi"}
        )
#        app.logger.error("FAILURE | portalapi | Unhandled exception occurred")
        return render_template("error.html", message="An unexpected error occurred."), 500

    @app.route('/')
    @github_login_required
    def index():
        try:
            items = get_items()
            item_view_model = viewmodel(items)
        except Exception as e:
            # Handle the MongoDB connection failure
            app.logger.error(
                "MongoDB connection error on index route.",
                extra={"status": "FAILURE", "component": "portalapi"}
            )
#            app.logger.error("FAILURE | portalapi | MongoDB connection error on index route.")
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
           
        app.logger.info(
            "Homepage rendered with posts.",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("RECOVERY | portalapi | Homepage rendered with posts.")
        return render_template('index.html', view_model=item_view_model, user=user, message=message)

   #     return render_template('index.html', view_model=item_view_model, user=user)

    @app.route('/add-data', methods=["POST"])
    @github_login_required
    def add_data():
  #      add_mongodata()
        try:
            add_trellodata()
        except Exception as e:
            app.logger.error(
                "Error adding Trello entry.",
                extra={"status": "FAILURE", "component": "portalapi"}
            )
#            app.logger.error("FAILURE | portalapi | Error adding Trello entry.")
        return redirect(url_for('index'))

    @app.route('/api')
    @github_login_required
    def api_request():
        customer = request.args.get('customer', default='*', type=str)
        salesorder = request.args.get('salesorder', default='*', type=str)
        engineer = request.args.get('engineer', default='*', type=str)
        try:
            add_mongodata(customer, salesorder, engineer)
            app.logger.info(
                "Trello and MongoDB entry added successfully.",
                extra={"status": "RECOVERY", "component": "portalapi"}
            )
#            app.logger.info("RECOVERY | portalapi | Trello and MongoDB entry added successfully.")
        except Exception as e:
            app.logger.error(
                "Error writing to MongoDb.",
                extra={"status": "FAILURE", "component": "portalapi"}
            )
#            app.logger.error("FAILURE | portalapi | Error writing to MongoDb.")
        try:
            add_trellodata(customer, salesorder, engineer)
        except Exception as e:
            app.logger.error(
                "Error adding Trello entry.",
                extra={"status": "FAILURE", "component": "portalapi"}
            )
#            app.logger.error("FAILURE | portalapi | Error adding Trello entry.")
        return redirect(url_for('index'))
            
    @app.route('/posts/<post_id>', methods=['DELETE'])
    def delete_post(post_id):
        try:
            posts = get_post_collection()
            result = posts.delete_one({"_id": ObjectId(post_id)})
            if result.deleted_count == 0:
                app.logger.error(
                    f"Error deleting post not found, with id: {post_id}.",
                    extra={"status": "FAILURE", "component": "portalapi"}
                )
#                app.logger.error(f"FAILURE | portalapi | Error deleting post not found, with id: {post_id}")
                return jsonify({"message": "Post not found"}), 404
            return jsonify({"message": "Post deleted successfully"}), 200
        except Exception as e:
            app.logger.error(
                f"Error deleting post with id: {post_id}.",
                extra={"status": "FAILURE", "component": "portalapi"}
            )
    #        app.logger.error(f"FAILURE | portalapi | Error deleting post with id: {post_id}")
            return jsonify({"message": str(e)}), 500
    
    @app.route('/login')
    @github_login_required
    def login():
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        token = github.blueprint.token["access_token"]
        del github.blueprint.token  # clear session
        app.logger.info(
            f"User logged out -  {token}",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info(f"User logged out -  {token}")
        print(f"User logged out: {token}")
        return redirect(url_for("index"))


    @app.route('/hpa')
    def hpa_loading():
        sum(i*i for i in range(10000000))
        app.logger.info(
            "Test Horizontal Pod Autoscaling.",
            extra={"status": "RECOVERY", "component": "portalapi"}
        )
#        app.logger.info("Test Horizontal Pod Autoscaling.")
        return redirect(url_for("index"))
    
    @app.route('/fail')
    def fail():
        raise RuntimeError("Deliberate crash to test logging.")

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    return app