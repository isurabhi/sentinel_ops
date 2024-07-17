# db/mongo_connector.py
import os
import dns.resolver
from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB_NAME

class MongoConnector:
    def __init__(self):
        print(os.environ)
        if os.getenv('DEBUG_MODE') == 'on':
            dns.resolver.default_resolver = dns.resolver.Resolver(configure=False) 
            dns.resolver.default_resolver.nameservers = ['20.236.44.162', '20.236.44.162']
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]