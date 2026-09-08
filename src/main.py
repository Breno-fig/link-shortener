
from .keygen import create_unique_key
from . import crud
from .schemas import URL_info #needed to have a Request Body parameter
from sqlalchemy.orm import Session 
from . import models, schemas
from .database import SessionLocal, engine

import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse


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


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/{url_key}")
def forward_to_url(
    url_key:str,
    request: Request,
    db: Session = Depends(get_db)
    ):

    if db_URL:= crud.get_db_url_by_key(db=db, url_key=url_key): #db URL receives the URL object that matches the key and is active, or None if no match is found
        return RedirectResponse(db_URL.target_url)
    else:
        raise_not_found(request)


@app.post("/url", response_model=URL_info) #response model is the model that will be returned to the user
def create_url(url: schemas.URL_base, db: Session = Depends(get_db)):
    if not validators.url(url.target_url): #checks if its a valid URL
        return raise_bad_request(message="URL not valid")
    
    db_URL = crud.create_db_url(db=db, url=url) #creates the URL in the database, updates the database and returns the URL object
    db_URL.url = db_URL.key 
    db_URL.admin_url = db_URL.secret_key
    
    return db_URL