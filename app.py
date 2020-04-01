from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import os

import os
import pickle
import paho.mqtt.client as mqtt
import numpy as np
import datetime

CLIENT_ID = '4665fab9-4827-40de-a1a6-36e538463bc4'
NETPIE_TOKEN = 'CXhbMLgUwHFZWKdt77AHEVAgio42f3k7'

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("@msg/predict_data/#", 0), ("@msg/sensor_data/#", 0)])
#def on_connect

@app.route('/api/sensor_data')
def api_sensor_data():

    device_id = request.args.get('device_id')
    label     = request.args.get('label')
    type      = request.args.get('type')
    print('{} {} {}'.format(device_id, label, type))

    try:
        q0 = SensorData.query.filter()
        if device_id:
            int(device_id)
            q1 = SensorData.query.filter_by(device_id=device_id)
            q0 = q0.intersect(q1)
        if label:
            int(label)
            q2 = SensorData.query.filter_by(label=label)
            q0 = q0.intersect(q2)
        if type:
            if type not in ['training', 'predicted']:
                raise Exception()
            q3 = SensorData.query.filter_by(type=type)
            q0 = q0.intersect(q3)
        #if
        print(q0.all())
    except:
        print('InvalidDataError')
        res = make_response('Bad request', 400)
        return res

    res = make_response('OK', 200) # Change to csv file

    return res
#def api_sensor_data

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
