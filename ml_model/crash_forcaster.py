from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import pandas as pd

class CRASHForecaster:
    def __init__(self, order=(7, 1, 1)):
        self.order = order
        self.model = None

    def fit(self, data):
        #train_data, test_data = train_test_split(data, test_size=splitperc, shuffle=False)
        # Fit the ARIMA model on the training data
        self.model = ARIMA(data, order=self.order)
        self.model = self.model.fit()
        #return test_data

    def predict(self, steps=1):
        # Forecast future values
        forecast = self.model.forecast(steps=steps)
        return forecast