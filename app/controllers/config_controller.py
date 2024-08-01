import pandas as pd
from flask import render_template, request

def settings():
    if request.method == 'POST':
        # Retrieve form data
        prod1Range = request.form.get('txtProd1Range', 1)
        prod1Email = request.form.get('txtProd1Email', 1)
        prod2Range = request.form.get('txtProd2Range', 1)
        prod2Email = request.form.get('txtProd2Email', 1)

        return render_template('config_saved.html' )
    else:
        # Render the forecast form template
        return render_template('config_alerts.html')