from fastapi import FastAPI, Response, status \
    , HTTPException  
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# model/schema/blueprint/definition
# we will be validating our user's input...
# data with this.
class Post(BaseModel):
    title: str
    content: str
    # default value of published
    # this is an optional field...
    # with a default value in schema
    published: bool = True
    #  fully optional field

# code for connecting to db
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


my_posts = [{"title": "Machine Learning", "content":  "Is a set of tools that tries to  \
             automate the intellectual tasks performed by humans", "id": 1},
             {'title': "Deep Learning", "content": "Is a subset of tools under machine \
              learning that learns progressive layers of increasingly meaningful \
              representation from the data, representations that takes us closer \
              to the actual output", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# homepage of our api
@app.get('/')
def root():
    # the return msg is converted to json...
    # and then gets sent back to the user
    return {'message': "Welcome to my API!!"}


@app.get('/posts')
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)
    return {'data': posts}


# if we want to change the default status code...
# we can add a status_code argument to the decorator...
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # inserting a new post in our sql database.
    # %s allows for input sanitization.
    # to prevent sql injection into our database.
    cur.execute("""INSERT INTO posts (title, content, published) 
                VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # to get that return value, we have to use cur.fetchone()
    new_post = cur.fetchone()
    # we have to commit the changes to the db
    conn.commit()
    print(new_post)
    
    return {'data': new_post}


# we converted the id to an int in the parameters.
# it's also a way of making  sure that the provided...
# id is an integer.
@app.get('/posts/{id}')
def get_posts(id:int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        # when the resource is not found
        # 404: Not Found
        # status gives us autocomplete for these status codes.
        # no need to hard code them
        # another smoother method is to raise an http exception

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

        # this is a much cleaner way of achieving the same results
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cur.fetchone()
    # anytime, we change a database. commit to it.
    print(deleted_post)
    conn.commit()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# we are almost done with all our crud operations
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""", 
                (post.title, post.content, post.published))
    updated_post = cur.fetchone()
    conn.commit()
    
    if updated_post == None:
        # you raise exceptins, not return them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Post Index not found")
    
    return {"data": updated_post}

# we are now at the end of our crud operation.