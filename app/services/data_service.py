# app/services/data_service.py
from db.mongo_connector import MongoConnector
from config.settings import MONGO_COLLECTION_NAME

class DataService:
    def __init__(self):
        self.connector = MongoConnector()

    def get_data(self):
        collection = self.connector.get_collection(MONGO_COLLECTION_NAME)
        return collection.find()