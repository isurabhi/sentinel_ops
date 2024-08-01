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

        # Drop rows with any missing values:
        #daily_crashes.dropna(inplace=True)

        train_data, test_data = train_test_split(daily_crashes, test_size=0.2, shuffle=False)

        # Fit the model and get the test data
        #arima_forecaster.fit(daily_crashes)
        arima_forecaster.fit(train_data)        
        
        # predictions = arima_forecaster.predict(steps=steps)
        forecast = arima_forecaster.predict(steps=steps)
        predictions = forecast.to_frame()

        #predictions_list = predictions.to_json(orient='records', date_format='iso') # predictions.iloc[0:steps]#.tolist()
        #train_data_list = daily_crashes.to_json(orient='records', date_format='iso') # test_data.iloc[0:steps]#.tolist()

        # Create a figure and axis with a black background
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#212529')
        ax.set_facecolor('#212529')
        
        #Plot graph of training set, Test set and Algorithm prediction on Test set
        plt.plot(train_data['total_crash'].resample('D').sum(), label='Historic')
        #plt.plot(test_data['total_crash'].resample('D').sum(), label='Current')
        plt.plot(predictions['predicted_mean'].resample('D').sum(), label='Forecasted', color='green')

        # Set the color of the tick labels and axis labels to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('silver')
        ax.yaxis.label.set_color('silver')
        # Set labels for axes
        plt.xlabel('Date')
        plt.ylabel('Total Crashes')
        plt.title('System Crash Forecast', color='silver')

        plt.legend(loc='upper center', ncol=3, facecolor='silver', edgecolor='white', framealpha=1)
        #plt.legend()

        # Save the figure
        plt.savefig('static/daily_total_crashes.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('crash_forecast.html', image_file='daily_total_crashes.png', steps=steps)
    else:
        # Render the forecast form template
        return render_template('crash_forecast_form.html')

def currentcrashes():
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

        # Drop rows with any missing values:
        #daily_crashes.dropna(inplace=True)

        train_data, test_data = train_test_split(daily_crashes, test_size=0.2, shuffle=False)

        # Fit the model and get the test data
        #arima_forecaster.fit(daily_crashes)
        arima_forecaster.fit(train_data)        
        
        # predictions = arima_forecaster.predict(steps=steps)
        forecast = arima_forecaster.predict(steps=steps)
        predictions = forecast.to_frame()

        #predictions_list = predictions.to_json(orient='records', date_format='iso') # predictions.iloc[0:steps]#.tolist()
        #train_data_list = daily_crashes.to_json(orient='records', date_format='iso') # test_data.iloc[0:steps]#.tolist()
        forecast_df_cpy = pd.DataFrame({
            'date': predictions.index,
            'total_crash': predictions['predicted_mean']
        })
        merged_df = pd.merge(test_data, forecast_df_cpy, on='date', suffixes=('_df1', '_df2'))
        condition_met_df = merged_df[merged_df['total_crash_df1'] > ((0.5 * merged_df['total_crash_df2']) + merged_df['total_crash_df2']) ]
        #html_table = condition_met_df.iloc[:, [0]].to_html(index=False, header=False, classes='table')
        #print(html_table)
        bootstrap_alerts = ''.join(f'<div class="alert alert-primary" role="alert">Notified that the actual data Spiked on: {value}</div>' for value in condition_met_df.iloc[:, 0])

        # Create a figure and axis with a black background
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#212529')
        ax.set_facecolor('#212529')
        
        #Plot graph of training set, Test set and Algorithm prediction on Test set
        plt.plot(train_data['total_crash'].resample('D').sum(), label='Historic')
        plt.plot(test_data['total_crash'].resample('D').sum(), label='Current')
        plt.plot(predictions['predicted_mean'].resample('D').sum(), label='Forecasted', color='green')

        # Set the color of the tick labels and axis labels to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('silver')
        ax.yaxis.label.set_color('silver')
        # Set labels for axes
        plt.xlabel('Date')
        plt.ylabel('Total Crashes')
        plt.title('System Crash Forecast', color='silver')

        plt.legend(loc='upper center', ncol=3, facecolor='silver', edgecolor='white', framealpha=1)
        #plt.legend()

        # Save the figure
        plt.savefig('static/daily_total_crashes.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('crash_forecast.html', image_file='daily_total_crashes.png',alert_data=bootstrap_alerts )