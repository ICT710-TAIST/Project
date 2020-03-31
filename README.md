# Getting Started
## Prerequisites
- Python3 
- pip
- virtualenv
- PostgreSQL
- Heroku CLI

## Setting Up
### 1. Clone project
```sh
$ git clone git@github.com:ICT710-TAIST/Project-Cloud.git
```
### 2. Create python virtual environment
```sh
$ cd Project-Cloud
$ python3 -m virtualenv .
$ source bin/activate
```
When you need to deactivate the virutal environment using this command
```sh
$ deactivate
```
### 3. Install dependencies
```sh
$ pip install -r requirements.txt
```
If you add new dependency, do not forget to add it to requirements.txt, you can do so by using this command
```sh
$ pip freeze > requirements.txt
```
### 4. Create database in your local machine
```sh
$ sudo createdb postgres
$ psql -d postgres # to check the database you have created.
$ export APP_SETTINGS="postgresql://localhost/postgres" # to set environment variable.
```

### 5. Create database tables
```sh
# to tell flask where to load shell context.
$ export FLASK_APP=manage.py 
$ flask shell
>>> db.create_all()
```
# Local Development
## Project Structure
- app.py
- config.py
- models.py
- mange.py
## CRUD (Using Flask-SQLAlchemy)
### Creating models
The following commands are not necessary during development. Unless you want to play around CRUD with flask shell. 
```sh
# to tell flask where to load shell context.
$ export FLASK_APP=manage.py 
$ flask shell
```
#### Adding device
```python
device = Device(
    device_name, 
    device_client_id)
db.session.add(device)
db.session.commit()
```
#### Adding sensor data
```python
sensor_data = SensorData(
    device_name, # foreign key
    roll,
    pitch,
    yaw,
    acc_x,
    acc_y,
    acc_z
)
db.session.add(sensor_data)
db.session.commit()
```
#### Reading models
```python
all_devices = Device.query.all()
all_sensor_data = SensorData.query.all()
```
#### Data Serialization
You can make a JSON of an instance by using serialization
```python
for device for Device.query.all():
    device.serialization()
```
## Database Migrations
```sh
# to tell flask where is our app
$ export FLASK_APP=app.py
$ flask db
$ flask db init # to start tracking our changes.
$ flask db migrate -m "init migration" # to start migration, this will create a new directory named migrations that will hold all the history.
$ flask db upgrade # to apply the migration to the database and change schema.
```

## Testing locally
```sh
$ heroku local
```

#  Deployment
You can push and merge to the master branch, heroku will automatically build the recently updated sourecode.
Deployed to heroku at https://taist-2020-heroku.herokuapp.com/ 

# Test 
* Test case: MQTT-Handler-TC-00
* Description:
    * MQTT Handler - Predict Incoming Data
* Test procedure:
    1. Use mqtt client to publish all possible valid and invalid data
    2. See log data from server
    3. Check database if the data was recorded

* Test data/device:
    * topic: @msg/predict_data/<device_id>
    * payload: roll,pitch,yaw,acc_x,acc_y,acc_z
        * device_id(Int)
        * roll(Int)
        * pitch(Int)
        * yaw(Int)
        * acc_x(Int)
        * acc_y(Int)
        * acc_z(Int)
* Expected results:
```
Valid:
    # Log from server
    <
        "device_id": device_id, 
        "roll": roll, 
        "pitch": pitch, 
        "yaw": yaw, 
        "acc_x": acc_x, 
        "acc_y": acc_y, 
        "acc_z": acc_z, 
        "label": predicted, # result from prediction, it could be '0' or '1'
        "type": "predict"
        "timestamp":, datetime
    >
    
    # Record from database
     id | device_id | roll | pitch | yaw | acc_x | acc_y | acc_z | label |   type   |         timestamp          
    ----+-----------+------+-------+-----+-------+-------+-------+-------+----------+----------------------------
      1 |         1 |    1 |     2 |   3 |     4 |     5 |     6 |     1 | predict | 2020-03-31 12:11:09.343793
```
    
```
Invalid:
    # Log from server
    ErrorInvalidData
    
    # Record from database
     id | device_id | roll | pitch | yaw | acc_x | acc_y | acc_z | label |   type   |         timestamp          
    ----+-----------+------+-------+-----+-------+-------+-------+-------+----------+----------------------------
    # No record added
```
* Actual results:
