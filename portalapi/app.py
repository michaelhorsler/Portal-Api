from flask import Flask, redirect, render_template, request
from portalapi.data.mongo_data import add_mongodata

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add-data', methods=["POST"])
    def add_data():
        add_mongodata()
        return redirect('/')

    return app
