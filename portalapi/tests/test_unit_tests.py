import pytest
from dotenv import load_dotenv, find_dotenv
from portalapi import app

@pytest.fixture
def client():
 # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
 # Create the new app.
    test_app = app.create_app()
 # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4


    