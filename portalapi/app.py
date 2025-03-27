from flask import Flask, redirect, render_template, request
from portalapi.data.mongo_data import add_mongodata, get_items
from portalapi.view_model import viewmodel

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        items = get_items()
        item_view_model = viewmodel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-data', methods=["POST"])
    def add_data():
        add_mongodata()
        return redirect('/')

    return app
