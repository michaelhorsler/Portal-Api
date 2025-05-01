import os
import requests

class TrelloCardCreationError(Exception):
    """Custom exception for Trello card creation failures."""
    pass

class MissingEnvVarError(Exception):
    """Custom exception for missing environment variables."""
    pass

def add_trellodata(customer=None, salesorder=None, engineer=None):
    customer = customer.strip() if customer else "Unknown Customer"
    salesorder = salesorder.strip() if salesorder else "No Sales Order"
    engineer = engineer.strip() if engineer else "Unassigned"

    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")
    list_id = os.getenv("TRELLO_TODO_LIST_ID")

    if not api_key or not api_token or not list_id:
        raise MissingEnvVarError("Missing required environment variables: TRELLO_API_KEY, TRELLO_API_TOKEN, or TRELLO_TODO_LIST_ID")

    url = "https://api.trello.com/1/cards"
    params = {
        'key': api_key,
        'token': api_token,
        'idList': list_id,
        'name': f"{salesorder} - {customer}",
        'desc': engineer
    }

    response = requests.post(url, params=params)

    if response.ok:
        print('✅ Card added successfully!')
        return True
    else:
        error_message = f"❌ Failed to create Trello card: {response.status_code} - {response.text}"
        raise TrelloCardCreationError(error_message)
