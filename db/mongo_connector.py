# db/mongo_connector.py
from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB_NAME

class MongoConnector:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]