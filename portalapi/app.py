from flask import Flask, redirect, render_template, request, url_for, session
from authlib.integrations.flask_client import OAuth
from portalapi.data.mongo_data import add_mongodata, apirequest, get_items
from portalapi.view_model import viewmodel
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "supersecret")

    # OAuth setup
    oauth = OAuth(app)
    github = oauth.register(
        name='github',
        client_id=os.environ['GITHUB_CLIENT_ID'],
        client_secret=os.environ['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    @app.route('/')
    def index():
        user = session.get('user')
        items = get_items()
        item_view_model = viewmodel(items)
        return render_template('index.html', view_model=item_view_model, user=user)

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

    @app.route('/login')
    def login():
        redirect_uri = url_for('authorize', _external=True)
        return github.authorize_redirect(redirect_uri)

    @app.route('/authorize')
    def authorize():
        token = github.authorize_access_token()
        user = github.get('user').json()
        session['user'] = user
        return redirect('/')

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect('/')

    return app