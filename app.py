from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

import os
import pickle
import paho.mqtt.client as mqtt
import numpy as np

import models

CLIENT_ID = 'f9cf386f-c6ab-4126-9eb7-96afa00c9095'
NETPIE_TOKEN = 'YNUUUmtUZpRaNMYaeLRTuvxCXrzkg86a'

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

model = pickle.load(open('machine_learning/model.pkl', 'rb'))

client = mqtt.Client(client_id=CLIENT_ID)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("@msg/predict_data/#", 0), ("@msg/sensor_data/#", 0)])
#def on_connect

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if 'predict_data' in msg.topic:
        payload = msg.payload.decode('utf-8')
        X = np.array([int(x) for x in payload.split(',')])
        device_id = int(msg.topic.split('/')[-1])
        roll    = int(X[0])
        pitch   = int(X[1])
        yaw     = int(X[2])
        acc_x   = int(X[3])
        acc_y   = int(X[4])
        acc_z   = int(X[5])
        label   = model.predict(X)
        type    = 'predicted'
        print(X)
        try:
            data = models.SensorData(device_id, roll, pitch, yaw, acc_x, acc_y, acc_z, label, type)
            print(data)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
#def on_message

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(NETPIE_TOKEN)
    client.connect("mqtt.netpie.io", 1883, 60)
    client.loop_start()
    app.run()
