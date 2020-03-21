from app import db
import datetime

class Device(db.Model):

    __tablename__ = 'device'

    device_name = db.Column(db.String(255), primary_key=True)
    device_client_id = db.Column(db.String(255))
    sensor_data = db.relationship(
        'SensorData',
        backref='device',
        lazy='dynamic'
    )

    def __init__(self, device_name, device_client_id):
        self.device_name = device_name
        self.device_client_id = device_client_id

    def __repr__(self):
        return '<device_name \'{}\'>'.format(self.device_name)

    def serialize(self):
        return {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'device_client_id': self.device_client_id
        }

class SensorData(db.Model):

    __table_name__ = 'sensor_data'

    sensor_data_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(255), db.ForeignKey('device.device_name'))
    roll        = db.Column(db.Float())
    pitch       = db.Column(db.Float())
    yaw         = db.Column(db.Float())
    acc_x       = db.Column(db.Float())
    acc_y       = db.Column(db.Float())
    acc_z       = db.Column(db.Float())
    timestamp   = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)

    def __init__(self, roll, pitch, yaw, acc_x, acc_y, acc_z):
        self.roll  = roll
        self.pitch = pitch
        self.yaw   = yaw
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z

    def __repr__(self):
        return '<roll {}, pitch {}, yaw {}, acc_x {}, acc_y {}, acc_z {}, timestamp {}>'.format(
            self.roll,
            self.pitch,
            self.yaw,
            self.acc_x,
            self.acc_y,
            self.acc_z,
            self.timestamp)

    def serialize(self):
        return {
            'device_name': self.device_name,
            'roll': self.roll,
            'pitch': self.pitch,
            'yaw': self.yaw,
            'acc_x': self.acc_x,
            'acc_y': self.acc_y,
            'acc_z': self.acc_z,
            'timestamp': self.timestamp
        }
