from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from  .. import models, schemas, database, utils

router = APIRouter(
    tags=['Authentication']
)

# schemas or pydantic models...
# ensures that data pushed in request...
# and in response follow a valid structure
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # trying to filter the user with...
    # the same email as requested
    user = db.query(models.User)\
        .filter(models.User.email == user_credentials.email).first()
    
    if not user:
        # 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Invalid credentials")
    # next, we also checked if the given password
    # is equal to the hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Invalid credentials")
    
    # create a token (JWT token)


    # return a token
    return {"token": "example token"}