from fastapi import FastAPI, Response, status \
    , HTTPException  
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

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
    rating: Optional[int] = None

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
    return {'data': my_posts}


# if we want to change the default status code...
# we can add a status_code argument to the decorator...
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # dict() is deprecated in base model.
    # instead use model_dump
    post_dict = post.model_dump()
    # adding an id field
    post_dict['id'] = randrange(0, 90000009)
    my_posts.append(post_dict)
    
    return {'data': post_dict}


# we converted the id to an int in the parameters.
# it's also a way of making  sure that the provided...
# id is an integer.
@app.get('/posts/{id}')
def get_posts(id:int):
    post = find_post(id)
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
    
    post_index = find_post_index(id)
    
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Post Index not found")
    
    my_posts.pop(post_index)
    # in the delete function, don't send any data back...
    # just send a 204 response code.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# we are almost done with all our crud operations
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    
    if post_index == None:
        # you raise exceptins, not return them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Post Index not found")
    # the post.dict() method is deprecated
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[post_index] = post_dict
    return {"data": post_dict}

