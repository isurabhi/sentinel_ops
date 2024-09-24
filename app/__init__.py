# app/__init__.py
from flask import Flask
from app.controllers import home_controller, detection_controller, forecast_controller, forcast_crashes_controller, config_controller, bsod_crash_controller

app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Create the Flask app instance

# Define route for the Home page
app.add_url_rule('/', 'Home', home_controller.home)

# Define routes for menu options
#app.add_url_rule('/forecast', 'Forecast', forecast_controller.forecast)
app.add_url_rule('/detect', 'Anomaly', detection_controller.detect_anomalies, methods=['POST'])
# app.add_url_rule('/menu1', 'menu1', controller1.menu1)
# app.add_url_rule('/menu2', 'menu2', controller2.menu2)
# app.add_url_rule('/menu3', 'menu3', controller3.menu3)

#app.route('/forecast', methods=['GET', 'POST'])
app.add_url_rule('/forecast', 'Forecast', forecast_controller.forecast, methods=['GET', 'POST'])
app.add_url_rule('/crashforecast', 'crashforecast', forcast_crashes_controller.crashforecast, methods=['GET', 'POST'])
app.add_url_rule('/bsodcrashforecast', 'bsodcrashforecast', bsod_crash_controller.bsodcrashforecast, methods=['GET', 'POST'])
app.add_url_rule('/bsodcrashdetails', 'bsodcrashdetails', bsod_crash_controller.bsodcrashdetails, methods=['GET', 'POST'])
app.add_url_rule('/config', 'Config', config_controller.alert_config, methods=['GET', 'POST'])
app.add_url_rule('/currentcrashes', 'currentcrashes', forcast_crashes_controller.currentcrashes, methods=['POST'])
app.add_url_rule('/get-machines', 'get-machines', bsod_crash_controller.get_crash_machines, methods=['GET'])