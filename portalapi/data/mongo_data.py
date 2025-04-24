import os
import pymongo
import ctypes
from portalapi.data.item import Item

_mock_collection = None

def set_mock_collection(mock):
    global _mock_collection
    _mock_collection = mock
#    print ("TESTING2")
#    print (_mock_collection)
    
def get_post_collection():
    global _mock_collection
    if _mock_collection is not None:
        return _mock_collection

    conn_string = os.getenv("MONGODBASE_CONN_STRING")
    mongodb = os.getenv("MONGODBASE")
 
    client = pymongo.MongoClient(conn_string)

    db = client[mongodb] # type: ignore

    return db.posts

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def add_mongodata(customer,salesorder,engineer):
    posts = get_post_collection()
    post = {
        "Customer": customer,
        "Sales_Order": salesorder,
        "Engineer": engineer
    }
    posts.insert_one(post).inserted_id

def get_items():
    posts = get_post_collection()
    items=[]
    for post in posts.find():
        item = Item.from_mongodb(post)
        items.append(item)
    return items

def apirequest(customer,salesorder,engineer):
# Note: Message box does not display when hosted on Azure. Causes error.
#    Mbox('API Request', customer, 1)
#    Mbox('API Request', salesorder, 1)
    add_mongodata(customer,salesorder,engineer)