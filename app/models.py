from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# creating our database table using sqlalchemy
# defining what our table in postgres will look like using  sqlalchemy
# sqlalchemy generates the tables but does not provide migrations
# for making future changes to the table.
# Alembic allows migrations/changes to db
class Post(Base):
    # how the table will be named inside postgres.
    __tablename__  =  'posts'

    # nullable if our field can't be blank.
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content  = Column(String,  nullable=False)
    published  =  Column(Boolean, server_default="TRUE", nullable=False)
    # timestamp with timezone
    # it can't be left blank
    # automatically set value
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text("now()"))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    # unique=True to prevent two emails registering twice.
    email = Column(String, nullable=False, unique=True)
    # we never store the actual password in our database...
    # we need to hash it.
    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))

