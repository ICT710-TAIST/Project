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
for data for all_sensor_data:
    all_sensor_data.serialization()
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
    
* Test procdure:
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
    
* Test procdure:
    1. Get valid messages from MQTT-Handler-TC-10
    2. Match input data with database model
    3. Store data in data base
    
* Test data/device:
    * Input data and database model
    
* Expected result:
   * Exception at invalid database model or input data return errorcode, valid payload return "Success"
    
