from pydantic import BaseModel, EmailStr
from datetime import datetime

# pydantic is used for validating...
# users input.
# model/schema/blueprint/definition
# we will be validating our user's input...
# data with this.
# class Post(BaseModel):
#     title: str
#     content: str
#     # default value of published
#     # this is an optional field...
#     # with a default value in schema
#     published: bool = True
#     #  fully optional field


# just like we can validate what a **request** should...
# look like, we can also validate what a **response**..
# should look like.

# request schema
# base class
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# sub class
# using inheritance
class PostCreate(PostBase):
    pass

# response schema
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    # make sure its a valid email and 
    # not just some random text.
    email : EmailStr
    password: str

class  UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # I don't really think we need this config in...
    # newer versions of fastapi
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str