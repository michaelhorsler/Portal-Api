import mongomock
import pytest
from portalapi import app
from dotenv import load_dotenv, find_dotenv
from portalapi.data.mongo_data import get_post_collection
from flask_dance.consumer.storage import MemoryStorage
from portalapi.oauth import blueprint

@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    storage = MemoryStorage({"access_token": "fake_token"})
    monkeypatch.setattr(blueprint, 'storage', storage)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

# Test 1: Mock index page with one post
def test_mock_index_page(client):
    posts = get_post_collection()
    post = {
        "Sales_Order": "typical",
        "Customer": "generic",
        "Engineer": "Bob",
    }
    posts.insert_one(post).inserted_id
    response = client.get('/')
    
    assert response.status_code == 200
    assert 'generic' in response.data.decode()

# Test 2: Mock index page with no posts (empty database)
def test_empty_database(client):
    # Make sure collection is empty
    posts = get_post_collection()
    posts.delete_many({})  # Clear any existing posts
    
    response = client.get('/')
    assert response.status_code == 200
    assert 'No posts available' in response.data.decode()  

# Test 3: Mock index page with multiple posts
def test_multiple_posts(client):
    posts = get_post_collection()
    post1 = {"Sales_Order": "SO123", "Customer": "Customer A", "Engineer": "Engineer A"}
    post2 = {"Sales_Order": "SO124", "Customer": "Customer B", "Engineer": "Engineer B"}
    post3 = {"Sales_Order": "SO125", "Customer": "Customer C", "Engineer": "Engineer C"}

    posts.insert_many([post1, post2, post3])
    response = client.get('/')

    assert response.status_code == 200
    assert 'Customer A' in response.data.decode()
    assert 'Customer B' in response.data.decode()
    assert 'Customer C' in response.data.decode()

# Test 4: Simulate MongoDB failure (e.g., connection failure)
def test_mongo_failure(client, monkeypatch):
    # Simulate MongoDB failure by patching `get_post_collection` to raise an error
    def mock_get_post_collection_failure():
        raise Exception("MongoDB connection failed")
    
    monkeypatch.setattr('portalapi.data.mongo_data.get_post_collection', mock_get_post_collection_failure)
    
    response = client.get('/')
    
    # Check if the status code is 500 (Internal Server Error)
    assert response.status_code == 500
    
    # Check if the error message is displayed
    assert "MongoDB connection failed" in response.data.decode()
    

