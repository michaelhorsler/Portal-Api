import mongomock
import pytest
#import globals

from portalapi import app
from dotenv import load_dotenv, find_dotenv
from portalapi.data.mongo_data import get_post_collection, set_mock_collection
from flask_dance.consumer.storage import MemoryStorage
from portalapi.oauth import blueprint

@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
#    globals.mocking="true"
#    global _mock_collection
#    set_mock_collection
    storage = MemoryStorage({"access_token": "fake_token"})
    monkeypatch.setattr(blueprint, 'storage', storage)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_mock_index_page(client):

    posts = get_post_collection()
    print (posts)
    post = {
            "Sales_Order": "typical",
            "Customer": "generic",
            "Engineer": "Bob",
        }
    posts.insert_one(post).inserted_id
#    global _mock_collection
#    set_mock_collection
    response = client.get('/')
    
    assert response.status_code == 200
    assert 'generic' in response.data.decode()