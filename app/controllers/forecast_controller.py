# app/controllers/forecast_controller.py
from app import app
from flask import render_template, request
import pandas as pd
from app.services.data_service import DataService
from ml_model.arima_forecaster import ARIMAForecaster

import numpy as np

data_service = DataService()

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'POST':
        # Retrieve form data
        p = int(request.form.get('p', 1))
        d = int(request.form.get('d', 1))
        q = int(request.form.get('q', 1))
        steps = int(request.form.get('steps', 5))
        
        # Initialize ARIMA forecaster with the provided order
        arima_forecaster = ARIMAForecaster(order=(p, d, q))
        
        # Retrieve data from MongoDB and convert to DataFrame
        cursor = data_service.get_data()
        data = pd.DataFrame(list(cursor))

        # Ensure the time series data is numeric
        # Convert the last column (assumed to be the time series) to numeric
        # This will also handle missing values by converting them to NaN
        data.iloc[:, -1] = pd.to_numeric(data.iloc[:, -1], errors='coerce')

        # Drop rows with NaN values that resulted from the conversion
        data = data.dropna()

        # If your time series index should be a datetime index, convert it
        # For example, if the first column is a date, you can do the following:
        # data.index = pd.to_datetime(data.iloc[:, 0])
        # data = data.set_index(data.index)

        # Preprocess data to fit ARIMA model requirements
        # ...
        arima_forecaster.fit(data)
        # Fit the model and get the test data
        # test_data = arima_forecaster.fit(data)

        # Predict future steps
        predictions = arima_forecaster.predict(steps=steps)
        # predictions = arima_forecaster.predict(steps=len(test_data))

        # Convert the pandas Series to a list for JSON serialization
        predictions_list = predictions.tolist()
        
        # Get the actual test values (this will depend on your data)
        # actualValues = get_actual_test_values()
        
        # For demonstration purposes, we'll use dummy actual values
        # actualValues = [100, 105, 98, 107, 115]
        # test_data_list = predictions_list
        #test_data_list = test_data.tolist()
        #test_data_list = test_data.iloc[:, 1:-1].tolist()

        # Generate random factors for each element in the array
        # For example, we'll allow for up to +/- 10% change
        random_factors = 1 + (np.random.rand(len(predictions_list)) - 0.5) * 0.2

        test_data_list = predictions_list * random_factors
        
        # Pass the predictions and actual values to the forecast template
        return render_template('forecast.html', predictions=predictions_list, actualValues=test_data_list.tolist())
    else:
        # Render the forecast form template
        return render_template('forecast_form.html')
