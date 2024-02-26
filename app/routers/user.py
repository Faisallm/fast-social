from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from  .. import models, utils, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hashing the user's password using passlib
    user.password = utils.hash(user.password)
    # unpacking values into the user model
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    # similar to returning *
    db.refresh(new_user)

    return new_user

# the purpose of this function is when we want to get the profile etc
@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id: {id} not found!")
    
    return user
