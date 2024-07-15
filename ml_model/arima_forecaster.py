# ml_model/arima_forecaster.py
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import pandas as pd

class ARIMAForecaster:
    def __init__(self, order=(1, 1, 1)):
        self.order = order
        self.model = None

    def fit(self, data):
        # Convert the cursor to a pandas DataFrame
        # data = pd.DataFrame(list(cursor))

        # Split the data into training and test sets (80% train, 20% test)
        # train_size = int(len(data) * 0.9)
        # train_data = data.iloc[:train_size, -1]
        # test_data = data.iloc[train_size:, -1]
        
        train_data, test_data = train_test_split(data, test_size=0.01, shuffle=False)
        
        # Assuming the last column of the DataFrame is the time series
        #time_series = data.iloc[:, -1]
        time_series = train_data.iloc[:, :-1]
        
        # Fit the ARIMA model
        #self.model = ARIMA(time_series, order=self.order)
        #self.model = self.model.fit()

        # Fit the ARIMA model on the training data
        self.model = ARIMA(time_series, order=self.order)
        self.model = self.model.fit()

        # Return the test data for later comparison
        # return test_data.iloc[:, -1]
        return test_data
        

    def predict(self, steps=1):
        # Forecast future values
        forecast = self.model.forecast(steps=steps)
        return forecast
