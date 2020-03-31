from app import db
import datetime

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
