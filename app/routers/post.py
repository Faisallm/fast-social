from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from  .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router  = APIRouter()

# in-memory database
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


@router.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


# if we want to change the default status code...
# we can add a status_code argument to the decorator...
@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # inserting a new post in our sql database.
    # %s allows for input sanitization.
    # to prevent sql injection into our database.
    # cur.execute("""INSERT INTO posts (title, content, published) 
    #             VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # # to get that return value, we have to use cur.fetchone()
    # new_post = cur.fetchone()
    # # we have to commit the changes to the db
    # conn.commit()
    # print(new_post)
    # we can unpack our schema using **
    # this is magic
    new_post = models.Post(**post.model_dump())
    # adding post and commiting to database.
    db.add(new_post)
    db.commit()
    # to be able to retrieve the new_post
    # similar to RETURNING *
    db.refresh(new_post)
    
    return new_post


# we converted the id to an int in the parameters.
# it's also a way of making  sure that the provided...
# id is an integer.
@router.get('/posts/{id}', response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id  == id).first()
    print(post)
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
    
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cur.fetchone()
    # # anytime, we change a database. commit to it.
    # print(deleted_post)
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    # if the post exist
    post.delete(synchronize_session=False)
    db.commit()
    # we don't return any data in the 'd' in crud:CRUD
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# we are almost done with all our crud operations
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #             (post.title, post.content, post.published, str(id)))
    
    # updated_post = cur.fetchone()
    # print(updated_post)
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post  = post_query.first()

    if updated_post == None:
        # you raise exceptions, not return them
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Post Index not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

# we are now at the end of our crud operation.