import os
import pymongo
from portalapi.data.item import Item

def get_post_collection():
    conn_string = os.getenv("MONGODBASE_CONN_STRING")
    mongodb = os.getenv("MONGODBASE")
 
    client = pymongo.MongoClient(conn_string)

    db = client[mongodb] # type: ignore

    posts = db.posts
    return posts

def add_mongodata():
    posts = get_post_collection()
    post = {
        "Customer": "Bills Hyd",
        "Sales_Order": "12345",
    }
    posts.insert_one(post).inserted_id

def get_items():
    posts = get_post_collection()
    items=[]
 #   for post in posts.find({"status": "To Do"}):
    for post in posts.find():
        item = Item.from_mongodb(post)
        items.append(item)
    #print (items)
    return items
