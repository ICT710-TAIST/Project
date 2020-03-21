# Getting Started
## Prerequisites
- Python3 
- pip
- virtualenv
- PostgreSQL
- Heroku CLI

## Installation
### 1. Clone Project
```sh
$ git clone git@github.com:ICT710-TAIST/Project-Cloud.git
```
### 2. Create python Virtual Environment
```sh
$ cd Project-Cloud
$ python3 -m virtualenv .
$ source bin/activate
```
When you need to deactivate the virutal environment using this command
```sh
$ deactivate
```
### 3. Install Dependencies
```sh
$ pip install -r requirements.txt
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
#### Adding device
```python
device = Device(
    device_name=device_name, 
    device_client=device_client_id)
db.session.add(device)
db.session.commit()
```
#### Adding sensor data
```python
sensor_data = SensorData(
    device_name=device_name, # foreign key
    roll=roll,
    pitch=pitch,
    yaw=yaw,
    acc_x=acc_x,
    acc_y=acc_y,
    acc_z=acc_z
)
db.session.add(sensor_data)
db.session.commit()
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
Deploy with heroku, you can push and merge to the master branch, heroku will automatically build the recent sourecode.
