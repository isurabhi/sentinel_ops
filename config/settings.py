# MongoDB configuration
#MONGO_URI = "mongodb://localhost:27017"
MONGO_URI = "mongodb+srv://isurabhi:mIR8ps4bDv0u7o@aisentinelops.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
MONGO_DB_NAME = "sentinel_ops_db"
MONGO_COLLECTION_NAME = "teams_freeze"
MONGO_COLLECTION_SYSTEM_CRASHES = "device_crashes"
MONGO_COLLECTION_ALERT_CONFIG = "alert_config"
MONGO_COLLECTION_ALERT = "spike_alerts"
MONGO_COLLECTION_BSOD_CRASH_COUNT = "BSOD_crash_count"
#-----------
CATERGORY_MAP = {
    'driver_hardware_errors': 'Driver and Hardware Errors',
    'memory_errors': 'Memory and Data Structure Errors',
    'storage_errors': 'File System and Storage Errors',
    'process_thread_errors': 'Process and Thread Management',
    'system_hardware_errors': 'System and Hardware Failures',
    'sync_iqrl_errors': 'Synchronization and IRQL Errors',
    'security_errors': 'Security and Integrity Failures',
    'generic_erros': 'Generic Errors',
    'unknown_errors': 'Unknown Category'
}