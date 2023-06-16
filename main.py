from flask import Flask,render_template,url_for,request,redirect, make_response, session
import random
from flask_caching import Cache
import json
import pandas as pd
from time import time
from random import random
from flask_mail import Mail, Message
import os
from scipy import signal
import numpy as np
import joblib

app = Flask(__name__)

file_path_storm = os.path.join(app.root_path,'clearWeather.csv')
file_path_fire = os.path.join(app.root_path,'NoFire.csv')
file_path_eq = os.path.join(app.root_path,'LogisticRegressionSeismometerNoeq.csv')
model_file_path = os.path.join(app.root_path,'LogisticRegressionSeismometer.joblib')
fire_model_file_path = os.path.join(app.root_path,'Decision_Tree_Classifier.joblib')
loaded_model = joblib.load(model_file_path)
loaded_fire_model = joblib.load(fire_model_file_path)

app.secret_key = 'your_secret_key'
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
app.config['MAIL_SERVER']='smtp.xyz.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abc@xyz.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#current_position = 0

mail = Mail(app)

@app.route('/send-email')
def send_email(event_type, depth, mag, wind, storm):
    print("event_type, depth, mag, wind, storm")
    print(event_type, depth, mag, wind, storm)
    message = Message(subject='URGENT: Data Center Emergency', 
    sender='abc@xyz.com', 
    recipients=['abc@xyz.com'])
    if(event_type == 0):
        message.subject='URGENT: Data Center Emergency - Earthquake Alert'
        message.body = f"""
        Subject: URGENT: Data Center Emergency - Earthquake Alert

        Dear Administrative Staff,

        We regret to inform you that an earthquake has been detected in the vicinity of our data center:
        
        - Magnitude: {mag}
        - Depth: {depth}


        Immediate action must be taken to ensure the safety of personnel and the integrity of our critical infrastructure. The following emergency measures should be implemented:

        1. Evacuation:
        - Initiate the evacuation protocol for all personnel present in the data center.
        - Follow designated evacuation routes to reach the designated assembly point.
        - Account for all personnel to ensure everyone has safely evacuated.

        2. Shutting Down Systems:
        - Designated staff should proceed with a systematic shutdown of critical systems and equipment to minimize potential damage.
        - Refer to the emergency shutdown procedures provided in the data center operations manual.
        - Ensure that power and cooling systems are safely turned off to prevent any hazards.

        3. Safety and Security:
        - Ensure that emergency exits are clear and accessible.
        - Assign responsible personnel to secure the data center premises during the evacuation.
        - Collaborate with emergency services and follow their instructions for additional safety measures.

        Please treat this matter with utmost urgency and ensure that all personnel are aware of the situation and the necessary actions to be taken. Regular updates should be provided to keep everyone informed about the status of the data center and any further instructions.

        If you have any questions or require immediate assistance, please contact the designated emergency response team or refer to the emergency contact numbers provided in the data center operations manual.

        Stay calm, stay safe, and prioritize the well-being of our personnel.

        Sincerely,

    """
    if(event_type == 1):

        message.subject='URGENT: Data Center Emergency - Fire Alarm and Prediction Alert'
        message.body = f"""
        Subject: URGENT: Data Center Emergency - Fire Alarm and Prediction Alert

            Dear Administrative Staff,

            We regret to inform you that our fire alarm and prediction system has detected a potential fire event in the vicinity of our data center. The safety of our personnel and the integrity of our critical infrastructure are of utmost importance. The following emergency measures must be implemented immediately:

            Data Center Humidity: {depth}
            Data Center Temperature: {mag}

            Emergency Procedures:

            1. Evacuation:
            - Initiate the evacuation protocol for all personnel present in the data center.
            - Follow designated evacuation routes to reach the designated assembly point.
            - Account for all personnel to ensure everyone has safely evacuated.
            
            2. System Shutdown:
            - Designated staff should proceed with a systematic shutdown of critical systems and equipment to minimize potential damage.
            - Refer to the emergency shutdown procedures provided in the data center operations manual.
            - Ensure that power and cooling systems are safely turned off to prevent any hazards.
            
            3. Safety and Security:
            - Ensure that emergency exits are clear and accessible.
            - Assign responsible personnel to secure the data center premises during the evacuation.
            - Collaborate with emergency services and follow their instructions for additional safety measures.
            - Please treat this matter with the utmost urgency and ensure that all personnel are aware of the situation and the necessary actions to be taken. Regular updates should be provided to keep everyone informed about the status of the data center and any further instructions.

            If you have any questions or require immediate assistance, please contact the designated emergency response team or refer to the emergency contact numbers provided in the data center operations manual.

            Stay calm, stay safe, and prioritize the well-being of our personnel.

            Sincerely,
    """
    if(event_type == 2):
        message.subject='URGENT: Data Center Emergency - OutBound Weather Conditions Alert'
        message.body = f"""
        Subject: URGENT: Data Center Emergency - OutBound Weather Conditions Alert

            Dear Administrative Staff,

            We regret to inform you that our Out-Bound weather conditions and prediction system has detected a potential Out-Bound weather conditions event in the vicinity of our data center. The safety of our personnel and the integrity of our critical infrastructure are of utmost importance. The following emergency measures must be implemented immediately:

            Humidity: {depth}
            Temperature: {mag}
            Wind Speed: {wind}

            Which may results in: {storm}

            Emergency Procedures:

            1. Evacuation:
            - Initiate the evacuation protocol for all personnel present in the data center.
            - Follow designated evacuation routes to reach the designated assembly point.
            - Account for all personnel to ensure everyone has safely evacuated.
            
            2. System Shutdown:
            - Designated staff should proceed with a systematic shutdown of critical systems and equipment to minimize potential damage.
            - Refer to the emergency shutdown procedures provided in the data center operations manual.
            - Ensure that power and cooling systems are safely turned off to prevent any hazards.
            
            3. Safety and Security:
            - Ensure that emergency exits are clear and accessible.
            - Assign responsible personnel to secure the data center premises during the evacuation.
            - Collaborate with emergency services and follow their instructions for additional safety measures.
            - Please treat this matter with the utmost urgency and ensure that all personnel are aware of the situation and the necessary actions to be taken. Regular updates should be provided to keep everyone informed about the status of the data center and any further instructions.

            If you have any questions or require immediate assistance, please contact the designated emergency response team or refer to the emergency contact numbers provided in the data center operations manual.

            Stay calm, stay safe, and prioritize the well-being of our personnel.

            Sincerely,
    """
    # print(message)
    mail.send(message)
    return 'Email sent!'
    
    
@app.route("/")
def home_view():
	return render_template('aa.html')
        #return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/changeEqFile", methods=['POST'])
def changeEqFilePath():
    # Receive integer property
    int_prop = request.form.get('int_prop')
    if int_prop is not None:
        int_prop = int(int_prop)
        # print(int_prop)
        # Use the integer property as needed

    file_path_eq = os.path.join(app.root_path,'LogisticRegressionSeismometer.csv') if int_prop == 1 else os.path.join(app.root_path,'LogisticRegressionSeismometerNoeq.csv') 
    
    cache.set('filepatheq', file_path_eq)
	#return "<h1>Welcome to Geeks for Geeks</h1>"
    return file_path_eq

@app.route("/changeFireFilePath", methods=['POST'])
def changeFireFilePath():
    # Receive integer property
    int_prop = request.form.get('int_prop')
    if int_prop is not None:
        int_prop = int(int_prop)
    # print("changeFireFilePathint_prop")
    # print("int_prop",str(int_prop))
        # Use the integer property as needed

    file_path_fire = os.path.join(app.root_path,'Fire.csv') if int_prop == 1 else os.path.join(app.root_path,'NoFire.csv') 

    # print(file_path_fire)
    cache.set('file_path_fire', file_path_fire)
	#return "<h1>Welcome to Geeks for Geeks</h1>"
    return file_path_fire

@app.route("/changeWeatherFilePath", methods=['POST'])
def changeWeatherFilePath():
    # Receive integer property
    int_prop = request.form.get('int_prop')
    if int_prop is not None:
        int_prop = int(int_prop)
    # print("changeWeatherFilePathint_prop")
    # print("int_prop",str(int_prop))
        # Use the integer property as needed

    file_path_storm = os.path.join(app.root_path,'stormWeather.csv') if int_prop == 1 else os.path.join(app.root_path,'clearWeather.csv') 

    # print(file_path_storm)
    cache.set('file_path_storm', file_path_storm)
	#return "<h1>Welcome to Geeks for Geeks</h1>"
    return file_path_storm

@app.route('/data', methods=["GET", "POST"])
def data():
    	
    current_position = cache.get('current_position')
    filepath_eq= cache.get('filepatheq')
    filepath_fire = cache.get('file_path_fire')
    filepath_storm = cache.get('file_path_storm')
    # print("file_path_fire1",filepath_fire)

    if filepath_eq is None:
        filepath_eq = file_path_eq # Set the initial position if not in cache
    if filepath_fire is None:
        filepath_fire = file_path_fire # Set the initial position if not in cache
    if filepath_storm is None:
        filepath_storm = file_path_storm # Set the initial position if not in cache
    if current_position is None:
        current_position = 0  # Set the initial position if not in cache
    # print("filepath_storm",filepath_storm)
    x = pd.read_csv(filepath_eq)
    # print("filepath_eq")
    # print(filepath_eq)
    y = pd.read_csv(filepath_fire)
    z = pd.read_csv(filepath_storm)
    # print(x.iloc[current_position,:-1])
    data = [time() * 100, int(x.iloc[current_position,2]), int(x.iloc[current_position,3]), int(x.iloc[current_position,5]),
            int(x.iloc[current_position,14]), int(x.iloc[current_position,15]), int(x.iloc[current_position,16]), 
            int(x.iloc[current_position,17]), int(x.iloc[current_position,18]), int(x.iloc[current_position,19]),
            int(y.iloc[current_position,1]), int(y.iloc[current_position,2]), int(y.iloc[current_position,7]), int(y.iloc[current_position,4]),
            int(z.iloc[current_position,0]), int(z.iloc[current_position,1]), int(z.iloc[current_position,2]), int(z.iloc[current_position,3]), int(z.iloc[current_position,4])]
    # print(data)
    
    pridiction( x.iloc[current_position,:-1], y.iloc[current_position,:-1])
    if(filepath_storm == os.path.join(app.root_path,'stormWeather.csv')):
        send_email(2, data[14], data[15], data[17], z.iloc[current_position,5])
    current_position = (current_position + 1)
    cache.set('current_position', current_position)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/pridiction', methods=["GET", "POST"])
def pridiction(data, fire_data):
    # print(fire_data)
    
    prediction = loaded_model.predict([data])

    fire_prediction = loaded_fire_model.predict([fire_data])
    # print("prediction")
    # print(prediction[0])
    eqmail = cache.get('eq_count')
    if eqmail is None:
        eqmail = 0
    fmail = cache.get('f_count')
    if fmail is None:
        fmail = 0
    print(int(data[3]))
    if prediction[0] != 3 :
        cache.set('eq_count', eqmail+1)
        if(eqmail+1 <=3 ):
            send_email(0, data[2],data[3],0,"")
    elif fire_prediction[0] == 1:
        cache.set('f_count', fmail+1)
        if(fmail+1 <=3 ):
            send_email(1, data[10],data[11],0,"")
    return ""

  
if __name__ == "__main__":	
	app.run(host = "127.0.0.1", port=8080,debug=True)
	


