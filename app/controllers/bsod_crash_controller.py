import pandas as pd
import matplotlib.pyplot as plt
from flask import render_template, request
from app.services.data_service import DataService
from ml_model.crash_forcaster import CRASHForecaster
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from config.settings import CATERGORY_MAP

data_service = DataService()

def bsodgetcrashdata(crash_type, start_date, end_date):
    if(crash_type == 'tot_crash'):
        filtered_documents = data_service.get_bsod_crash_data(start_date, end_date)
    else:
        filtered_documents = data_service.get_bsod_crash_details(crash_type, start_date, end_date)

    data = pd.DataFrame(list(filtered_documents))
    # Set the 'system_crash_date' column as the index of the DataFrame
    data.set_index('system_crash_date', inplace=True)
    # Sort the DataFrame by the index (timestamp) if needed
    data.sort_index(inplace=True)

    return data

def bsodcrashforecast():
    if request.method == 'POST':
    # Retrieve form data
        p = 5 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        steps = int(request.form.get('steps', 7))
        crash_type = request.form.get('crash_type')

        data = bsodgetcrashdata(crash_type, start_date, end_date)

        if(crash_type == 'tot_crash'):
            tot_series_data = data
        else: 
            tot_series_data = data['system_crash_count']

        # Initialize ARIMA forecaster with the provided order        
        tot_arima_forecaster = CRASHForecaster(order=(p, d, q))
        tot_arima_forecaster.fit(tot_series_data)
        tot_forecast = tot_arima_forecaster.predict(steps=steps)
        tot_predictions = tot_forecast.to_frame()

        # Convert your dates to a format that can be serialized to JSON
        # dates = [date.strftime('%Y-%m-%d') for date in data.index]
        if isinstance(tot_series_data, pd.DataFrame):
            total_crash_data = tot_series_data.sum(axis=1).resample('D').sum().tolist()
        else:
            total_crash_data = tot_series_data.resample('D').sum().tolist()
        #total_crash_data = tot_series_data.resample('D').sum().tolist()
        total_crash_forecasted_data = tot_predictions['predicted_mean'].resample('D').sum().tolist()

        dates = [date.strftime('%Y-%m-%d') for date in data.index]
        last_date = datetime.strptime(dates[-1], '%Y-%m-%d')

        # Add 10 more days to the 'dates' array
        for i in range(1, steps):
            new_date = last_date + timedelta(days=i)
            dates.append(new_date.strftime('%Y-%m-%d'))

        if crash_type in data.columns:
            series_data = data[crash_type].resample('D').sum()
            arima_forecaster_d = CRASHForecaster(order=(p, d, q))
            arima_forecaster_d.fit(series_data)
            forecast = arima_forecaster_d.predict(steps=steps)
            history_data = series_data.tolist()
            forecast_data = forecast.tolist()
            #dates = [date.strftime('%Y-%m-%d') for date in data.index]
            # Prepare the data for the frontend
            chart_data = {
                'labels': dates,
                'datasets': [
                    {'label': 'Total Crash', 'data': total_crash_data, 'borderColor': 'blue'},
                    {'label': 'Forecast Crash', 'data': [None] * len(total_crash_data) + total_crash_forecasted_data, 'borderColor': 'green'},
                    {'label': f'{crash_type} History', 'data': history_data, 'borderColor': 'orange'},
                    {'label': f'{crash_type} Forecast', 'data': [None] * len(history_data) + forecast_data, 'borderColor': 'yellow'}
                ]
            }   
        else:
            # Prepare the data for the frontend
            # dates = [date.strftime('%Y-%m-%d') for date in data.index]
            chart_data = {
                'labels': dates,
                'datasets': [
                    {'label': 'Total Crash', 'data': total_crash_data, 'borderColor': 'blue'},
                    {'label': 'Forecasted Crash', 'data': [None] * len(total_crash_data) + total_crash_forecasted_data, 'borderColor': 'green'}
                ]
            }

        return render_template('bsod_crash_forcast1.html', chart_data=chart_data)
    else:
        # Render the forecast form template
        cat_map = CATERGORY_MAP
        start_dt = datetime.strptime("2024-01-01", '%Y-%m-%d')
        end_dt = datetime.strptime("2024-08-31", '%Y-%m-%d')
        return render_template('bsod_crash_form.html', default_start_date="2024-01-01", default_end_date="2024-08-31", category_map=cat_map)

def bsodcrashforecast1():
    if request.method == 'POST':
        # Retrieve form data
        p = 5 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        steps = int(request.form.get('steps', 7))
        crash_type = request.form.get('crash_type')
        #print(f"p: {p}, d: {d}, q: {q}, steps: {steps}!")
        print(f"start_date: {start_date}, end_date: {end_date}, crash_type: {crash_type}, steps: {steps}!")
        # Initialize ARIMA forecaster with the provided order        
        arima_forecaster = CRASHForecaster(order=(p, d, q))
        if(crash_type == 'tot_crash'):
            filtered_documents = data_service.get_bsod_crash_data(start_date, end_date)
            data = pd.DataFrame(list(filtered_documents))
            # Set the 'system_crash_date' column as the index of the DataFrame
            data.set_index('system_crash_date', inplace=True)
            # Sort the DataFrame by the index (timestamp) if needed
            data.sort_index(inplace=True)
            arima_forecaster.fit(data)
            tot_forecast = arima_forecaster.predict(steps=steps)
            tot_predictions = tot_forecast.to_frame()
        else:
            filtered_documents = data_service.get_bsod_crash_details(crash_type, start_date, end_date)
            data = pd.DataFrame(list(filtered_documents))
            # Set the 'system_crash_date' column as the index of the DataFrame
            data.set_index('system_crash_date', inplace=True)
            # Sort the DataFrame by the index (timestamp) if needed
            data.sort_index(inplace=True)
            tot_series_data = data['system_crash_count'].resample('D').sum()
            arima_forecaster.fit(tot_series_data)
            tot_forecast = arima_forecaster.predict(steps=steps)
            tot_predictions = tot_forecast.to_frame()

        if(crash_type == 'tot_crash'):
            #train_data, test_data = train_test_split(data, test_size=0.20, shuffle=False)
            #print (train_data)
            #arima_forecaster.fit(data)
            #forecast = arima_forecaster.predict(steps=steps)
            #predictions = forecast.to_frame()

            # Create a figure and axis with a black background
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#212529')
            ax.set_facecolor('#212529')
        
            #Plot graph of training set, Test set and Algorithm prediction on Test set
            plt.plot(data['system_crash_count'].resample('D').sum(), label='Total Crash')     
            plt.plot(tot_predictions['predicted_mean'].resample('D').sum(), label='Forecasted', color='green')

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
            image_file_name='bsod_total_crashes.png'

        else:
            if crash_type in data.columns:
                # Resample data for the selected crash type
                series_data = data[crash_type].resample('D').sum()
                            # Fit the model and make a forecast
                arima_forecaster_d = CRASHForecaster(order=(p, d, q))
                arima_forecaster_d.fit(series_data)
                forecast = arima_forecaster_d.predict(steps=steps)
                            # Plot the forecast
                #plt.figure(figsize=(10, 5))
                    # Create a figure and axis with a black background
                fig, ax = plt.subplots(figsize=(13, 6))
                fig.patch.set_facecolor('#212529')
                ax.set_facecolor('#212529')
        
                plt.plot(data['system_crash_count'].resample('D').sum(), label='Total Crash')     
                plt.plot(tot_predictions['predicted_mean'].resample('D').sum(), label='Forecasted', color='green')
                plt.plot(series_data, label=f'{crash_type} History', color='orange')
                plt.plot(forecast, label='Forecasted', color='yellow')
                plt.legend()
                plt.xlabel('Date')
                plt.ylabel('Crash Counts')
                plt.title(f'BSOD {crash_type} Forecast', color='silver')

                # Set the color of the tick labels and axis labels to white
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.xaxis.label.set_color('silver')
                ax.yaxis.label.set_color('silver')

                #plt.legend(loc='upper left', ncol=2, facecolor='silver', edgecolor='white', framealpha=1, bbox_to_anchor=(1, 1))
                plt.legend(loc='upper left', ncol=1, facecolor='silver', edgecolor='white', framealpha=1, bbox_to_anchor=(1, 1))

                # Save the plot to a file
                plt.savefig('static/bsod_crash_forecast.png')
                plt.close()
                image_file_name = 'bsod_crash_forecast.png'

        return render_template('bsod_crash_forcast.html', image_file=image_file_name, steps=steps)
    else:
        # Render the forecast form template
        cat_map = CATERGORY_MAP
        start_dt = datetime.strptime("2024-01-01", '%Y-%m-%d')
        end_dt = datetime.strptime("2024-08-31", '%Y-%m-%d')
        return render_template('bsod_crash_form.html', default_start_date="2024-01-01", default_end_date="2024-08-31", category_map=cat_map)
    
def bsodcrashdetails():
    if request.method == 'POST':
        # Retrieve form data
        p = 5 # int(request.form.get('p', 1))
        d = 1 # int(request.form.get('d', 1))
        q = 1 # int(request.form.get('q', 1))
        steps = int(request.form.get('steps', 7))
        print(f"p: {p}, d: {d}, q: {q}, steps: {steps}!")

        filtered_documents = data_service.get_bsod_crash_details()
        data = pd.DataFrame(list(filtered_documents))

        # Set the 'system_crash_date' column as the index of the DataFrame
        data.set_index('system_crash_date', inplace=True)
        # Sort the DataFrame by the index (timestamp) if needed
        data.sort_index(inplace=True)

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
        plt.savefig('static/bsod_crashes_details.png', bbox_inches='tight')
        plt.close()  # Close the figure to free up memory

        return render_template('bsod_crash_forcast.html', image_file='bsod_crashes_details.png', steps=steps)
    else:
        # Render the forecast form template
        return render_template('bsod_crash_form.html')