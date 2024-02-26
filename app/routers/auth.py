from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from  .. import models, schemas, database, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

# schemas or pydantic models...
# ensures that data pushed in request...
# and in response follow a valid structure
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # trying to filter the user with...
    # the same email as requested

    # OAuth2PasswordRequestForm returns the email as the username
    user = db.query(models.User)\
        .filter(models.User.email == user_credentials.username).first()
    
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
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return a token.
    # bearer refers to the type of token.
    return {"access_token": access_token, "token_type": "bearer"}