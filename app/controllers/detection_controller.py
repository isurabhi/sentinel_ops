# app/controllers/detection_controller.py
#from flask import Flask, render_template, request, redirect, url_for
from app import app
from flask import render_template, request
from app.services.data_service import DataService
from ml_model.anomaly_detector import AnomalyDetector

#app = Flask(__name__, template_folder='../../templates')  # Create the Flask app instance

data_service = DataService()
anomaly_detector = AnomalyDetector()

@app.route('/', methods=['GET'])  # Define the route for the index page
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])  # Define the route for the detection
def detect_anomalies():
    data = data_service.get_data()
    # Preprocess data and convert to appropriate format for ML model
    # For example, convert data to a pandas DataFrame or a NumPy array
    # X = preprocess(data)
    # predictions = anomaly_detector.predict(X)
    # For demonstration purposes, we'll use dummy predictions
    predictions = [1, -1, 1, -1]  # 1 for normal, -1 for anomaly
    # Redirect to the index page with the results
    return render_template('index.html', predictions=predictions)
