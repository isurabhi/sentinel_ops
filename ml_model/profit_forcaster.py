import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from prophet import Prophet

class ProphetForecaster:
    def __init__(self):
        self.model = None
    
    def fit(self, data):
        self.model = Prophet()
        self.model = self.model.fit()

    def predict(self, steps=30):
        # Forecast future values
        future = self.model.make_future_dataframe(periods=steps)
        future.tail()
        forecast = self.model.predict(future)
        #forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        return forecast