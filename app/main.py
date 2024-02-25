from fastapi import FastAPI, Response, status \
    , HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import  models, schemas, utils
from .database import engine, get_db
from .routers import post, user



# connecting the sqlachemy models and our pg database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# code for connecting to db
# previous code for connecting when using pure sql...
# with no sqlalchemy
while True:
    try:
        # connecting to a postgres db
        # RealDictCursor added inorder to get...
        # column name.
        conn = psycopg2.connect(host='localhost', database='fastapi-social', 
                                user='postgres', password='Faisal',
                                cursor_factory=RealDictCursor)
        # allows us to execute sql statements
        cur  = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to Database Failed!")
        print("Error: ", error)
        # wait for 2 seconds before trying to reconnect
        time.sleep(2)

# including router objects for each model.
# this is how we break our posts into seperate files.
app.include_router(post.router)
app.include_router(user.router)

# homepage of our api
@app.get('/')
def root():
    # the return msg is converted to json...
    # and then gets sent back to the user
    return {'message': "Welcome to Faisal's API!!"}

