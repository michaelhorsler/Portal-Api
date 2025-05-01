import pytest
import requests
import os
from dotenv import load_dotenv, find_dotenv
from unittest import mock
from portalapi import app
from portalapi.data.trello_data import MissingEnvVarError, add_trellodata, TrelloCardCreationError

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client
    
# 1. Success Test: Simulate successful Trello card creation
@mock.patch('requests.post')
def test_post_success(mock_post):
    mock_response = mock.Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    result = add_trellodata(customer="Test Customer", salesorder="SO123", engineer="Test Engineer")
    
    assert result is True
    assert mock_post.called
    called_url = mock_post.call_args[0][0]
    called_params = mock_post.call_args[1]['params']

    assert called_url == "https://api.trello.com/1/cards"
    assert called_params['name'] == "SO123 - Test Customer"
    assert called_params['desc'] == "Test Engineer"

# 2. Failure Test: Simulate Trello card creation failure (401 Unauthorized)
@mock.patch('requests.post')
def test_post_failure(mock_post):
    mock_response = mock.Mock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_post.return_value = mock_response

    with pytest.raises(TrelloCardCreationError) as exc_info:
        add_trellodata(customer="Fail Customer", salesorder="SO_FAIL", engineer="Fail Engineer")

    assert "401" in str(exc_info.value)
    assert "Unauthorized" in str(exc_info.value)
    assert mock_post.called

# 3. Network Error: Simulate a network error, like a timeout
@mock.patch('requests.post')
def test_network_error(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")
    
    with pytest.raises(requests.exceptions.Timeout):
        add_trellodata(customer="Test Customer", salesorder="SO123", engineer="Test Engineer")

# 4. Invalid response format from Trello (e.g., non-JSON response)
@mock.patch('requests.post')
def test_invalid_response_format(mock_post):
    mock_response = mock.Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = "Not JSON"  # Simulating a non-JSON response
    mock_post.return_value = mock_response

    # When the response is invalid, the function should still succeed.
    result = add_trellodata(customer="Test Customer", salesorder="SO123", engineer="Test Engineer")
    
    assert result is True  # We expect success even if the response is not JSON (this would be part of production error handling)
    assert mock_post.called

# 5. Empty parameters (None or empty strings passed as arguments)
@mock.patch('requests.post')
def test_empty_parameters(mock_post):
    mock_response = mock.Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    # Test with empty values for customer, salesorder, and engineer
    result = add_trellodata(customer="", salesorder="", engineer="")

    # Assert: Check the fallback behavior when empty strings are passed
    assert result is True
    assert mock_post.called
    called_params = mock_post.call_args[1]['params']
    
    # Check if fallback values ("Unknown Customer", "No Sales Order", "Unassigned") were used
    assert called_params['name'] == "No Sales Order - Unknown Customer"
    assert called_params['desc'] == "Unassigned"

# 6. Missing environment variables (API key, token, or list ID)
@mock.patch('requests.post')
def test_missing_env_vars(mock_post):
    # Remove environment variables to simulate missing values
    del os.environ['TRELLO_API_KEY']
    del os.environ['TRELLO_API_TOKEN']
    del os.environ['TRELLO_TODO_LIST_ID']

    # Test MissingEnvVarError is raised
    with pytest.raises(MissingEnvVarError) as exc_info:
        add_trellodata(customer="Test Customer", salesorder="SO123", engineer="Test Engineer")

    # Check the exception message
    assert "Missing required environment variables" in str(exc_info.value)
    
