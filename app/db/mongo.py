'''
Connect to mongo database
'''

from pymongo.mongo_client import MongoClient

CONNECTION_STRING = "mongodb://mongo:mongo@mongo"

client = MongoClient('mongodb://mongo', username='mongo', password='mongo')
db = client['app']

if __name__ == "__main__":
    db = client.test
    collection = db.items
    item = {
        "body": "Hello"
    }
    db_item = collection.insert_one(item).inserted_id
    print(db_item)
