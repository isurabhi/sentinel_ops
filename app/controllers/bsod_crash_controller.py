import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template, request
from app.services.data_service import DataService
from ml_model.crash_forcaster import CRASHForecaster
from sklearn.model_selection import train_test_split

data_service = DataService()

def bsodcrashforecast():
    if request.method == 'POST':
        # Retrieve form data
        p = 5 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        steps = int(request.form.get('steps', 7))
        print(f"p: {p}, d: {d}, q: {q}, steps: {steps}!")

        # Initialize ARIMA forecaster with the provided order
        arima_forecaster = CRASHForecaster(order=(p, d, q))

        filtered_documents = data_service.get_bsod_crash_data()
        data = pd.DataFrame(list(filtered_documents))

        # Set the 'system_crash_date' column as the index of the DataFrame
        data.set_index('system_crash_date', inplace=True)
        # Sort the DataFrame by the index (timestamp) if needed
        data.sort_index(inplace=True)

        # train_data, test_data = train_test_split(data, test_size=0.20, shuffle=False)
        # arima_forecaster.fit(train_data)
        # forecast = arima_forecaster.predict(steps=steps)
        # predictions = forecast.to_frame()

        # Create a figure and axis with a black background
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#212529')
        ax.set_facecolor('#212529')
        
        #Plot graph of training set, Test set and Algorithm prediction on Test set
        plt.plot(data['system_crash_count'].resample('D').sum(), label='Total Crash')
        plt.plot(data['driver_hardware_errors'].resample('D').sum(), label='Driver Errors')
        plt.plot(data['memory_errors'].resample('D').sum(), label='Memory Errors')
        plt.plot(data['storage_errors'].resample('D').sum(), label='Storage Errors')
        plt.plot(data['process_thread_errors'].resample('D').sum(), label='Thread Errors')
        plt.plot(data['system_hardware_errors'].resample('D').sum(), label='System Errors')
        plt.plot(data['sync_iqrl_errors'].resample('D').sum(), label='IQRL Errors')
        plt.plot(data['security_errors'].resample('D').sum(), label='Security Errors')
        plt.plot(data['generic_erros'].resample('D').sum(), label='Generic Errors')
        plt.plot(data['unknown_errors'].resample('D').sum(), label='Uncategorised')
        #plt.plot(predictions['predicted_mean'].resample('D').sum(), label='Forecasted', color='green')
         
        # Set the color of the tick labels and axis labels to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.xaxis.label.set_color('silver')
        ax.yaxis.label.set_color('silver')
        # Set labels for axes
        plt.xlabel('Date')
        plt.ylabel('Crash Counts')
        plt.title('BSOD Crashes', color='silver')

        #plt.legend(loc='upper center', ncol=3, facecolor='silver', edgecolor='white', framealpha=1)
        plt.legend(loc='upper left', ncol=2, facecolor='silver', edgecolor='white', framealpha=1, bbox_to_anchor=(1, 1))
        #plt.legend()

        # Save the figure
        plt.savefig('static/bsod_total_crashes.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('bsod_crash_forcast.html', image_file='bsod_total_crashes.png', steps=steps)
    else:
        # Render the forecast form template
        return render_template('bsod_crash_form.html')
