# app/__init__.py
from flask import Flask

app = Flask(__name__, template_folder='../templates')  # Create the Flask app instance

# Import the controllers to register the routes
from app.controllers import detection_controller
from app.controllers import forecast_controller