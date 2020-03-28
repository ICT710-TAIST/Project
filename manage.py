from app import app, db, migrate
from models import SensorData

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, SensorData=SensorData, migrate=migrate)
