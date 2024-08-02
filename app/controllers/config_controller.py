import pandas as pd
from flask import render_template, request
from app.models.alert_config import AlertConfig

def alert_config():
    if request.method == 'POST':
        # Retrieve form data
        prod1Range = request.form.get('txtProd1Range', 1)
        prod1Email = request.form.get('txtProd1Email', 1)
        prod2Range = request.form.get('txtProd2Range', 1)
        prod2Email = request.form.get('txtProd2Email', 1)

        alert_config1 = AlertConfig()
        alert_config1.set('ms_freeze_alert',prod1Range,prod1Email)
        id1 = alert_config1.save()
        print(id1)
        alert_config2 = AlertConfig()
        alert_config2.set('system_crash_alert',prod2Range,prod2Email)
        id2 = alert_config2.save()
        print(id2)

        data = alert_config1.get_alert_config()
        data_df = pd.DataFrame(data)
        html_table = data_df.to_html(index=False, header=False, classes='table')

        return render_template('config_saved.html', alert_config=html_table)    
    else:
        # Render the forecast form template
        return render_template('config_alerts.html')

def get_alerts():
    alert_data = AlertConfig()
    data = alert_data.g .get_data()
    return data