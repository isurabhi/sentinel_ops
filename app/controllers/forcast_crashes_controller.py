import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template, request
from app.services.data_service import DataService
from ml_model.crash_forcaster import CRASHForecaster
from sklearn.model_selection import train_test_split

data_service = DataService()

def crashforecast():
    if request.method == 'POST':
        # Retrieve form data
        p = 7 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        steps = int(request.form.get('steps', 7))
        print(f"p: {p}, d: {d}, q: {q}, steps: {steps}!")

        # Initialize ARIMA forecaster with the provided order
        arima_forecaster = CRASHForecaster(order=(p, d, q))

        filtered_documents = data_service.get_system_crash_data()
        data = pd.DataFrame(list(filtered_documents))

        # Set the 'timestamp' column as the index of the DataFrame
        data.set_index('time_stamp', inplace=True)
        # Sort the DataFrame by the index (timestamp) if needed
        data.sort_index(inplace=True)

        print(f"data len: {len(data)}")

        # Group by the date part alone and count the number of crashes per day
        data['date'] = pd.to_datetime(data['date'])
        data['date'] = data['date'].dt.normalize()
        daily_crashes = data.groupby('date').size().reset_index(name='total_crash')
        #daily_crashes['date'] = pd.to_datetime(daily_crashes['date'], errors='coerce')
        #daily_crashes['total_crash'] = np.asarray(daily_crashes['total_crash'], dtype=np.float64)#pd.to_numeric(daily_crashes['total_crash'], errors='coerce')
        daily_crashes.set_index('date', inplace=True)
        daily_crashes = daily_crashes.asfreq('D')
        daily_crashes['total_crash'] = pd.to_numeric(daily_crashes['total_crash'], errors='coerce')

        train_data, test_data = train_test_split(daily_crashes, test_size=0.2, shuffle=False)

        # Fit the model and get the test data
        #arima_forecaster.fit(daily_crashes)
        arima_forecaster.fit(train_data)        
        
        # predictions = arima_forecaster.predict(steps=steps)
        forecast = arima_forecaster.predict(steps=steps)
        predictions = forecast.to_frame()

        #predictions_list = predictions.to_json(orient='records', date_format='iso') # predictions.iloc[0:steps]#.tolist()
        #train_data_list = daily_crashes.to_json(orient='records', date_format='iso') # test_data.iloc[0:steps]#.tolist()

        
        #Plot graph of training set, Test set and Algorithm prediction on Test set
        plt.figure(figsize=(12, 6))
        #plt.plot(daily_crashes['total_crash'], label='Training Data')
        plt.plot(train_data['total_crash'].resample('D').sum(), label='Training Data')
        plt.plot(test_data['total_crash'].resample('D').sum(), label='Test Data')
        plt.plot(predictions['predicted_mean'].resample('D').sum(), label='Forecasted Data', color='green')
        plt.xlabel('Date')
        plt.ylabel('Total Crashes')
        plt.title('ARIMA Model - Total Crashes Forecast')
        plt.legend()
        #plt.show()
        # Save the figure
        plt.savefig('static/daily_total_crashes.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('crash_forecast.html', image_file='daily_total_crashes.png' )
    else:
        # Render the forecast form template
        return render_template('crash_forecast_form.html')