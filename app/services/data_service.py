# app/services/data_service.py
from db.mongo_connector import MongoConnector
from config.settings import MONGO_COLLECTION_NAME
from config.settings import MONGO_COLLECTION_SYSTEM_CRASHES
from config.settings import MONGO_COLLECTION_ALERT_CONFIG
from config.settings import MONGO_COLLECTION_ALERT
from config.settings import MONGO_COLLECTION_BSOD_CRASH_COUNT
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

    def get_bsod_crash_data(self, start_date, end_date):
        collection = self.connector.get_collection(MONGO_COLLECTION_BSOD_CRASH_COUNT)

        #date_string = "2023-08-01"
        #date_format = "%Y-%m-%d"
        #comparison_date = datetime.strptime(date_string, date_format)

        # Convert dates to datetime objects
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        # Define the query to filter the documents
        #query = {"device_country": country, 'device_city': {'$nin': [None, ""]}}
        query = {'system_crash_date': {'$gte': start_datetime, '$lte': end_datetime}}
        #query = {"device_country": country}
        
        # Define the projection to select specific fields (1 to include, 0 to exclude)
        projection = {"_id": 0, "system_crash_date": 1, "system_crash_count": 1 }
        
        # Execute the query and projection
        filtered_documents = collection.find(query, projection)
        #filtered_documents = collection.find(query)
        # Iterate over the filtered documents and print them
        # for doc in filtered_documents:
        #    print(doc)
        return filtered_documents
    
    def get_bsod_crash_details(self, crash_type, start_date, end_date):
        collection = self.connector.get_collection(MONGO_COLLECTION_BSOD_CRASH_COUNT)

        # Convert dates to datetime objects
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        # Define the query to filter the documents
        query = {'system_crash_date': {'$gte': start_datetime, '$lte': end_datetime}}
        
        # Define the projection to select specific fields (1 to include, 0 to exclude)
        projection = {"_id": 0, "system_crash_date": 1, "system_crash_count": 1, crash_type: 1 }
        
        # Execute the query and projection
        filtered_documents = collection.find(query, projection)
        return filtered_documents
    
    def get_bsod_crash_machines(self, crash_date, crash_type):
        collection = self.connector.get_collection('BSOD')
        crash_datetime = datetime.strptime(crash_date, '%Y-%m-%d')
        if(crash_type == 'Total Crashes'):
            query = {
                'system_crash_date': {'$eq': crash_datetime},
                'Category': {'$eq': crash_type}
                }
        else:
            query = {
                'system_crash_date': {'$eq': crash_datetime}
                }
        #projection = {"_id": 0, "system_crash_date": 1, "device_name": 1, "crash_label": 1 }
        #filtered_documents = collection.find(query, projection)
        #return filtered_documents

        # Aggregation pipeline to group by crash_label and count device occurrences
        pipeline = [
            {'$match': query},
            {'$group': {
                '_id': '$crash_label',  # Group by crash_label
                'device_count': {'$sum': 1},  # Count device occurrences
                'devices': {'$push': '$device_name'}  # Collect device names under each crash_label
            }},
            {'$project': {
                '_id': 0,
                'crash_label': '$_id',  # Rename _id to crash_label
                'device_count': 1,  # Include the count of devices
                'devices': 1  # Include the list of devices
            }}
        ]        
        grouped_documents = collection.aggregate(pipeline)
        return list(grouped_documents)  # Convert the aggregation result to a list