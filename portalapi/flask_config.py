import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'very_secret_key')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
    LOGS_LEVEL = os.environ.get('LOGS_LEVEL')
    LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN')
