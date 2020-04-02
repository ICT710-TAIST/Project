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
$ export DATABASE_URL="postgresql://localhost/postgres" # to set environment variable.
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
- mange.py
## CRUD (Using Flask-SQLAlchemy)
### Creating models
The following commands are not necessary during development. Unless you want to play around CRUD with flask shell. 
```sh
# to tell flask where to load shell context.
$ export FLASK_APP=manage.py 
$ flask shell
```
#### Adding sensor data
```python
sensor_data = SensorData(
    device_id, 
    roll,
    pitch,
    yaw,
    acc_x,
    acc_y,
    acc_z,
    label,
    type # 'training' or 'predicted'

)
db.session.add(sensor_data)
db.session.commit()
```
#### Reading models
```python
all_sensor_data = SensorData.query.all()
```
#### Data Serialization
You can make a JSON of an instance by using serialization
```python

for sensor_data for SensorData.query.all():
    sensor_data.serialization()
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
#### Test case: MQTT-Handler-TC-10
* Describtion:
    * Check if message is valid
    
* Test procedure:
    1. Start MQTT client
    2. Create different messages with valid and invalid messages
    3. Send messages to MQTT server
    
* Test data/device:
    * Payloda of MQTT @msg/sensor_data/<device_id>
    
* Expected result:
   * Exception at invalid payload return errorcode, valid payload return message
    
#### Test case: MQTT-Handler-TC-11
* Describtion:
    * Check if input data can store in database
    
* Test procedure:
    1. Get valid messages from MQTT-Handler-TC-10
    2. Match input data with database model
    3. Store data in data base
    
* Test data/device:
    * Input data and database model
    
* Expected result:
   * Exception at invalid database model or input data return errorcode, valid payload return "Success"

#### Test case: MQTT-Handler-TC-12
* Describtion:
    * Check if data get stored right in database
    
* Test procedure:
    1. Get valid messages from MQTT-Handler-TC-10
    2. Store data with MQTT-Handler-TC-11
    3. Load data from database and match with the message
    
* Test data/device:
    * Database
    
* Expected result:
   * Exception if data doesn't match or data can't get load return errorcode, valid payload return "Success"
    
#### Test case: MQTT-Handler-TC-00
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
      1 |         1 |    1 |     2 |   3 |     4 |     5 |     6 |     1 | predict  | 2020-03-31 12:11:09.343793
```
    
```
Invalid:
    # Log from server
    InvalidDataError
    
    # Record from database
     id | device_id | roll | pitch | yaw | acc_x | acc_y | acc_z | label |   type   |         timestamp          
    ----+-----------+------+-------+-----+-------+-------+-------+-------+----------+----------------------------
    # No record added
```
* Actual results:

#### Test case: RESTful-API-csv-00

* Describtion:
    * For analysts to get the sensor data for analysis
    * To test exporting csv file using RESTful API
    
* Test procedure:
    1. Connect database and server to get the recorded and predicted data
    2. Export sensor data to csv file 
    
* Test data/device:
    * Check sensor data in csv file
    * Check database and csv file
    * Requests and Responses
        * 200 : A csv file including column names
        * 500 : Internal server error

* Expected result:
   * Sensor data as csv file