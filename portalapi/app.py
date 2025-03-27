from flask import Flask, redirect, render_template, request
from portalapi.data.mongo_data import add_mongodata, apirequest, get_items
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

    @app.route('/api')
    def api_request():
        customer = request.args.get('customer', default = '*', type = str)
        salesorder = request.args.get('salesorder', default = '*', type = str)
        # new_customer = request.form.get('customer')
        apirequest(customer,salesorder)
        return redirect('/')

    return app
