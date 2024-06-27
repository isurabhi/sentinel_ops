# ml_model/anomaly_detector.py
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest()

    def train(self, X):
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)