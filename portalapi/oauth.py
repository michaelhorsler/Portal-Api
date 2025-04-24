import os
from flask_dance.contrib.github import make_github_blueprint
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

blueprint = make_github_blueprint(
    client_id = os.getenv('OAUTH_CLIENT_ID'),
    client_secret = os.getenv('OAUTH_CLIENT_SECRET'),

)
