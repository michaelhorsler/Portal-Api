import mongomock
import pytest

from portalapi import app
from dotenv import load_dotenv, find_dotenv
from portalapi.data.mongo_data import get_post_collection
from flask_dance.consumer.storage import MemoryStorage

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    storage = MemoryStorage({"access_token": "fake_token"})
 #   monkeypatch.setattr('storage', storage)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_mock_index_page(client):

    posts = get_post_collection()
    post = {
            "Sales_Order": "typical",
            "Customer": "generic",
        }
    posts.insert_one(post).inserted_id

    response = client.get('/')
    
    assert response.status_code == 200
    assert 'generic' in response.data.decode()