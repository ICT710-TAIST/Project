from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

model = pickle.load(open('machine_learning/model.pkl', 'rb'))

client = mqtt.Client(client_id=CLIENT_ID)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
    client.connect("mqtt.netpie.io", 1883, 60)
    client.loop_start()

