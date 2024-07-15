# app/controllers/forecast_controller.py
#from app import app
import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template, request
from app.services.data_service import DataService
from ml_model.crash_forcaster import CRASHForecaster
from sklearn.model_selection import train_test_split

import numpy as np

data_service = DataService()


def forecast():
    if request.method == 'POST':
        # Retrieve form data
        p = 7 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        country = request.form.get('country')
        steps = int(request.form.get('steps', 7))
        print(f"p: {p}, d: {d}, q: {q}, steps: {steps}!")

        # Initialize ARIMA forecaster with the provided order
        arima_forecaster = CRASHForecaster(order=(p, d, q))
        
        # Retrieve data from MongoDB and convert to DataFrame
        # cursor = data_service.get_data()
        # data = pd.DataFrame(list(cursor))
        filtered_documents = data_service.get_country_data(country) #('India')
        data = pd.DataFrame(list(filtered_documents))
        
        # Set the 'timestamp' column as the index of the DataFrame
        data.set_index('event_date', inplace=True)
        # Sort the DataFrame by the index (timestamp) if needed
        data.sort_index(inplace=True)

        print(f"data len: {len(data)}")

        # Group by the date part alone and count the number of crashes per day
        #data['event_date'] = pd.to_datetime(data['event_date'])
        #data['event_date'] = data['event_date'].dt.normalize()
        #grouped_df = data.groupby(['event_date', 'device_os', 'device_city'])['number_of_freezes'].sum().reset_index()
        grouped_df = data.groupby(['event_date'])['number_of_freezes'].sum().reset_index()
        grouped_df['event_date'] = grouped_df['event_date'].dt.normalize()
        #model_data = grouped_df
        #print(f"model_data len: {len(model_data)}")

        grouped_df.set_index('event_date', inplace=True)
        grouped_df = grouped_df.asfreq('D')
        grouped_df['number_of_freezes'] = pd.to_numeric(grouped_df['number_of_freezes'], errors='coerce')

        train_data, test_data = train_test_split(grouped_df, test_size=0.1, shuffle=False)

        # Drop rows with NaN values that resulted from the conversion
        # data = data.dropna()

        # Fit the model and get the test data
        #arima_forecaster.fit(daily_crashes)
        arima_forecaster.fit(train_data) 
        print(f"test data rows: {len(test_data)}")

        # Predict future steps
        forecast = arima_forecaster.predict(steps=steps)
        predictions = forecast.to_frame()

        #Plot graph of training set, Test set and Algorithm prediction on Test set
        plt.figure(figsize=(12, 6))
        #plt.plot(daily_crashes['total_crash'], label='Training Data')
        plt.plot(train_data['number_of_freezes'].resample('D').sum(), label='Training Data')
        plt.plot(test_data['number_of_freezes'].resample('D').sum(), label='Test Data')
        plt.plot(predictions['predicted_mean'].resample('D').sum(), label='Forecasted Data', color='green')
        plt.xlabel('Date')
        plt.ylabel('Total Teams Freezes')
        plt.title('ARIMA Model - Total MS Teams Forecast')
        plt.legend()
        #plt.show()
        # Save the figure
        plt.savefig('static/daily_total_teams_freezes.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('forecast.html', image_file='daily_total_teams_freezes.png' )

        # Convert the pandas Series to a list for JSON serialization
        #predictions_list = predictions.iloc[0:steps].tolist()
        
        # Get the actual test values (this will depend on your data)
        # actualValues = get_actual_test_values()
        
        # For demonstration purposes, we'll use dummy actual values
        # actualValues = [100, 105, 98, 107, 115]
        # test_data_list = predictions_list
        ### test_data_list = test_data.tolist()
        #test_data_list = test_data.iloc[0:steps, -1].tolist()

        # Generate random factors for each element in the array
        # For example, we'll allow for up to +/- 10% change
        # random_factors = 1 + (np.random.rand(len(predictions_list)) - 0.5) * 0.2

        # test_data_list = predictions_list * random_factors
        #print(f"predictions_list :{len(predictions_list)}, test_data_list:{len(test_data_list)}")
        
        # Pass the predictions and actual values to the forecast template
        #return render_template('forecast.html', predictions=predictions_list, actualValues=test_data_list)
    else:
        # Render the forecast form template
        return render_template('forecast_form.html')
