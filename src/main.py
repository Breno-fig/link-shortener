import secrets, string

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


@app.post("/url", response_model=URL_info) #response model is the model that will be returned to the user
def create_url(url: schemas.URL_base, db: Session = Depends(get_db)):
    if not validators.url(url.target_url): #checks if its a valid URL
        return raise_bad_request(message="URL not valid")
    
    characters = string.ascii_letters
    key = ''.join(secrets.choice(characters)for i in range(5)) #generates a random 5 character string based on characters
    secret_key = ''.join(secrets.choice(characters)for i in range(8)) #same but for the admin
    db_URL = models.URL( #url that will be inserted into the database
        target_url=url.target_url, #db_URL receives it, but the function does not return it in the JSON response 
        key = key,
        secret_key = secret_key
    )
    db.add(db_URL)
    db.commit()
    db.refresh(db_URL) #refreshes the db_URL object with the new data from the database
    db_URL.url = key
    db_URL.admin_url = secret_key
    return db_URL