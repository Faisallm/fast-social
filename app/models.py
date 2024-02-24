from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

# creating our database table using sqlalchemy
# defining what our table in postgres will look like using  sqlalchemy
class Post(Base):
    # how the table will be named inside postgres.
    __tablename__  =  'posts'

    # nullable if our field can't be blank.
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content  = Column(String,  nullable=False)
    published  =  Column(Boolean, default=True)
