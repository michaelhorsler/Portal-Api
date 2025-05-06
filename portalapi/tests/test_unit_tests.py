import pytest
from dotenv import load_dotenv, find_dotenv
from portalapi import app
from portalapi.data.item import Item
from portalapi.view_model import viewmodel

test_items = [
    Item(1, "Customer 1", "12345", "Engineer 1"),
    Item(2, "Customer 2", "", ""),
    Item(3, "", "", "Engineer 2"),
    Item(4, "" , "", "Engineer 3")
]

def test_view_model_return_engineer_only():
    view_model = viewmodel(test_items)
    engineer_items = view_model.engineer_items
    assert len(engineer_items) == 3

def test_view_model_return_customer_only():
    view_model = viewmodel(test_items)
    customer_items = view_model.customer_items
    assert len(customer_items) == 2

def test_view_model_return_salesorder_only():
    view_model = viewmodel(test_items)
    salesorder_items = view_model.salesorder_items
    assert len(salesorder_items) == 1


    