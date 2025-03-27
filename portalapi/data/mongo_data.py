import os
import pymongo
import ctypes
from portalapi.data.item import Item

def get_post_collection():
    conn_string = os.getenv("MONGODBASE_CONN_STRING")
    mongodb = os.getenv("MONGODBASE")
 
    client = pymongo.MongoClient(conn_string)

    db = client[mongodb] # type: ignore

    posts = db.posts
    return posts

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def add_mongodata(customer,salesorder):
    posts = get_post_collection()
    post = {
        "Customer": customer,
        "Sales_Order": salesorder,
    }
    posts.insert_one(post).inserted_id

def get_items():
    posts = get_post_collection()
    items=[]
    for post in posts.find():
        item = Item.from_mongodb(post)
        items.append(item)
    return items

def apirequest(customer,salesorder):
    Mbox('API Request', customer, 1)
    Mbox('API Request', salesorder, 1)
    add_mongodata(customer,salesorder)