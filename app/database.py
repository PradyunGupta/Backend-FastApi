import time # to make a retry connection to the database within a specified timeframe
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 # connecting to our database
from psycopg2.extras import RealDictCursor # to return the data in a dictionary format
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# connecting to our database
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='ronaldo@1',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("Error",error)
#         time.sleep(2)







