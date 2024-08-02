from app.services.data_service import DataService

data_service = DataService()

# Model
class AlertConfig:
    def __init__(self):
        self.alertName = ""
        self.variance = 0
        self.email = ""

    def set(self, alertName, variance, email):
        self.alertName = alertName
        self.variance = variance
        self.email = email

    def save(self):
        alert_config = {
            'alert_name': self.alertName,
            'variance': self.variance,
            'email': self.email
        }

        inserted_id = data_service.save_alert_config(alert_config)
        return inserted_id
    
    def get_alert_config(self):
        data = data_service.get_alert_config()
        return data
    
    def get_alerts(self):
        data = data_service.get_spike_alerts()
        return data