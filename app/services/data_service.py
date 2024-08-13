# app/services/data_service.py
from db.mongo_connector import MongoConnector
from config.settings import MONGO_COLLECTION_NAME
from config.settings import MONGO_COLLECTION_SYSTEM_CRASHES
from config.settings import MONGO_COLLECTION_ALERT_CONFIG
from config.settings import MONGO_COLLECTION_ALERT
from datetime import datetime

class DataService:
    def __init__(self):
        self.connector = MongoConnector()

    def get_data(self):
        collection = self.connector.get_collection(MONGO_COLLECTION_NAME)
        return collection.find()

    def get_country_data(self, country):
        collection = self.connector.get_collection(MONGO_COLLECTION_NAME)

        date_string = "2024-05-30"
        date_format = "%Y-%m-%d"
        comparison_date = datetime.strptime(date_string, date_format)

        # Define the query to filter the documents
        #query = {"device_country": country, 'device_city': {'$nin': [None, ""]}}
        query = {"device_country": country, 'device_city': {'$nin': [None, ""]},'event_date': {'$gt': comparison_date}}
        #query = {"device_country": country}
        
        # Define the projection to select specific fields (1 to include, 0 to exclude)
        projection = {"_id": 0, "event_date": 1, "device_os": 1, "device_city": 1, "number_of_freezes": 1 }
        
        # Execute the query and projection
        filtered_documents = collection.find(query, projection)
        # Iterate over the filtered documents and print them
        # for doc in filtered_documents:
        #    print(doc)
        return filtered_documents

    def get_system_crash_data(self):
        #date_string = "2024-02-28"
        #date_format = "%Y-%m-%d"
        #comparison_date = datetime.strptime(date_string, date_format)
        #query = {'system_crash_time': {'$gt': comparison_date}}
        collection = self.connector.get_collection(MONGO_COLLECTION_SYSTEM_CRASHES)
        return collection.find()
        #return collection.find(query)
    
    def get_spike_alerts(self):
        collection = self.connector.get_collection(MONGO_COLLECTION_ALERT)
        return collection.find()
    
    def get_alert_config(self):
        collection = self.connector.get_collection(MONGO_COLLECTION_ALERT_CONFIG)
        return collection.find()
    
    def save_alert_config(self, alert):
        collection = self.connector.get_collection(MONGO_COLLECTION_ALERT_CONFIG)
        result = collection.insert_one(alert)
        return result.inserted_id
