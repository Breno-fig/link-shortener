from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import get_settings

engine = create_engine( #main communication with the database
    get_settings().db_url, #parameter to the db url
    connect_args={"check_same_thread": False} #allows multiple threads to access the database 
)
SessionLocal = sessionmaker( #factory for creating new Session objects used to access the database through the engine
    autocommit=False, 
    autoflush=False, 
    bind=engine #connect sessions to the engine
)
Base = declarative_base() #register the models with the database and create the tables in the database
