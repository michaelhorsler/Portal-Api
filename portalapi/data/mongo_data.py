import os
import pymongo

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
        "Customer": "Bobs Hyd",
        "Sales Order": "12345",
    }
    posts.insert_one(post).inserted_id