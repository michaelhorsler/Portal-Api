import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'very_secret_key')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
    LOGS_LEVEL = os.environ.get("LOGS_LEVEL", "INFO")
    LOGGLY_TOKEN = os.environ.get("LOGGLY_TOKEN")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_ADMINS = os.environ.get("MAIL_ADMINS", "").split(",")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

    FEATURE_FLAGS = {
    "ENABLE_ADD_DATA": False,
    "ENABLE_TRELLO_SYNC": True,
    "ENABLE_HPA_ROUTE": True,
    "ENABLE_DELETE_POST": True,
    }