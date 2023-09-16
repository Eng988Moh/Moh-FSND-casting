# Moh-FSND-casting-agency
 
Final project to complete the Full Stack Nanodegree from Udacity


In this application you can:

1. Dispaly Actors/Movies
2. Delete Actors/Movies
3. Add new Actors/Movies
4. Edit existing Actors/Movies

We are always working on enchancing the users' experience and we are always welcoming your improvments.

## Dependancies

-Python 3

To install the ```requirements``` , in the root directory run ```pip install -r requirements.txt```

### Backend

To run the application locally

Note 1: you can create a local Postgres database for the main app to run using the command ```createdb capstone``` and update the URI for the database in the code.

Note 2: On the first run in ```app.py``` uncomment these two lines:

```python
with app.app_context():
   db_drop_and_create_all()
```

In the root directory run ```bash setup.sh``` then run ```flask run --reload``` or manually run the following commands:
bash:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --reload
```
source setup.sh to activate it
===================================


## Testing
You MUST have a local database for tests,to create a one run the command ```createdb capstone_test```.
In the root directory of the project run ```python test_app.py```
The test file will automatically fill the database and drop all the tables after it is done.

## API Documentation

### Getting Started

Base URL: (hosted on Render) "https://casting-agency-0o2z.onrender.com" || (running locally) ```https://localhost:5000/```

Authentication
-

There is three roles in this application and it is required to have the apropiate role to use the endpoints

Roles:
-

    CASTINGASSISTANT:
        Can view actors and movies
    CASTINGDIRECTOR:
        Add  an actor from the database
        Modify actors or movies
    CASTINGPRODUCER:
        All permissions granted to a CASTINGPRODUCER

You need to set the environment variable to use with your Bearer token:

bash:

```bash
export TOKEN=YOUR_TOKEN
```


## Endpoint Library

GET /Itsworking
-

Shows the state of the application.

```bash
curl https://casting-agency-0o2z.onrender.com/Itsworking

```

Response Example:

### {"Its working fine":true}



GET /actors  |  GET /movies
-
postman test examples

### GET Response
Get http://127.0.0.1:5000/actors
{
    "actors": {
        "age": 41,
        "gender": "Male",
        "id": 2,
        "name": "Ryan Gosling"
    },
    "current_page": {
        "age": 52,
        "gender": "Female",
        "id": 1,
        "name": "Cate Blanchett"
    },
    "success": true,
    "total_actors": 252
}


