import secrets

from .schemas import URL_info #needed to have a Request Body parameter
from sqlalchemy.orm import Session 
from . import models, schemas
from .database import SessionLocal, engine

import validators
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db(): #manages one db session per request
    db = SessionLocal() #db is our section to access the database
    try:
        yield db #yield pauses the function when it's called,
                 #and when next(get_db) is called, 
                 #it returns the db session, and when the request
                 #is finished, it resumes the function and closes 
                 #the db session
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/url")
def create_url(url: URL_info):  #URL is a pydantic model that validates the input data 
                                #     // it's a REQUEST BODY
    if not validators.url(url.target_url): #checks if its a valid URL
        return raise_bad_request(message="URL not valid")
    return {"TODO: create dabase entry for": url.target_url} 
    