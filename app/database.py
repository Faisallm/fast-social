from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# this file will handle sqlalchemy connection with our database.

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Faisal@localhost/fastapi-social"

engine  = create_engine  (SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    # this is where we get a connection to our db.
    # through  sqlalchemy
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()