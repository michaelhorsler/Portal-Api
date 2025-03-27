import pytest
from dotenv import load_dotenv, find_dotenv
from portalapi import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client
    
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4


    