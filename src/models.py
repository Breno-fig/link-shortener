from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class URL(Base):
    __tablename__ = "urls" #name of the table in the database

    id = Column(Integer, primary_key=True) #id is the primary key of the table
    key = Column(String, unique=True, index=True) #keeps the random string that will be used to access the URL
    secret_key = Column(String, unique=True, index=True) #another key but for admins to check the URL info (statistics, edit, etc)
    target_url = Column(String, index=True) #keeps the original URL (doesn't make sense for it to be unique)
    is_active = Column(Boolean, default=True) 
    clicks = Column(Integer, default=0)