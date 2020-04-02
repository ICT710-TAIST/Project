from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

import os

import pickle
import paho.mqtt.client as mqtt
import numpy as np
import datetime

CLIENT_ID = 'f9cf386f-c6ab-4126-9eb7-96afa00c9095'
NETPIE_TOKEN = 'YNUUUmtUZpRaNMYaeLRTuvxCXrzkg86a'

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

model = pickle.load(open('machine_learning/model.pkl', 'rb'))

client = mqtt.Client(client_id=CLIENT_ID)

class SensorData(db.Model):

    __table_name__ = 'sensor_data'

    id          = db.Column(db.Integer(), primary_key=True)
    device_id   = db.Column(db.Integer())
    roll        = db.Column(db.Integer())
    pitch       = db.Column(db.Integer())
    yaw         = db.Column(db.Integer())
    acc_x       = db.Column(db.Integer())
    acc_y       = db.Column(db.Integer())
    acc_z       = db.Column(db.Integer())
    label       = db.Column(db.Integer())
    type        = db.Column(db.String())
    timestamp   = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)

    def __init__(self, device_id, roll, pitch, yaw, acc_x, acc_y, acc_z, label, type):
        self.device_id = device_id
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.label = label
        self.type  = type

    def __repr__(self):
        return '<device_id {}, roll {}, pitch {}, yaw {}, acc_x {}, acc_y {}, acc_z {}, label {}, type {}, timestamp {}>'.format(
            self.device_id,
            self.roll,
            self.pitch,
            self.yaw,
            self.acc_x,
            self.acc_y,
            self.acc_z,
            self.label,
            self.type,
            self.timestamp)

    def serialize(self):
        return {
            'device_id': self.device_id,
            'roll': self.roll,
            'pitch': self.pitch,
            'yaw': self.yaw,
            'acc_x': self.acc_x,
            'acc_y': self.acc_y,
            'acc_z': self.acc_z,
            'label': self.label,
            'type' : self.type,
            'timestamp': self.timestamp
        }
#class SensorData

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("@msg/predict_data/#", 0), ("@msg/sensor_data/#", 0)])
#def on_connect

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("topic: {}\tpayload: {}".format(msg.topic, msg.payload.decode('utf-8')))
    if 'sensor_data' in msg.topic:
        #Validate incoming data
        try:
            payload = msg.payload.decode('utf-8')
            X = np.array([int(x) for x in payload.rstrip('\x00').split(',')])
            device_id = int(msg.topic.split('/')[-1])
            roll    = int(X[0])
            pitch   = int(X[1])
            yaw     = int(X[2])
            acc_x   = int(X[3])
            acc_y   = int(X[4])
            acc_z   = int(X[5])
            label   = int(X[6])
            type    = 'training'
        except:
            print("InvalidDataError")
            return

        #Record the data
        try:
            data = SensorData(device_id, roll, pitch, yaw, acc_x, acc_y, acc_z, label, type)
            print(data)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
            return
    #if sensor_data

    if 'predict_data' in msg.topic:
        #Validate incoming data
        try:
            payload = msg.payload.decode('utf-8')
            X = np.array([int(x) for x in payload.rstrip('\x00').split(',')])
            device_id = int(msg.topic.split('/')[-1])
            roll    = int(X[0])
            pitch   = int(X[1])
            yaw     = int(X[2])
            acc_x   = int(X[3])
            acc_y   = int(X[4])
            acc_z   = int(X[5])
            label   = int(model.predict(X))
            type    = 'predicted'
        except:
            print("InvalidDataError")
            return

        #Record the data
        try:
            data = SensorData(device_id, roll, pitch, yaw, acc_x, acc_y, acc_z, label, type)
            print(data)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
            return
    #if predict_data
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
