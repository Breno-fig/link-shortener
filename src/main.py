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


@app.get("/{url_key}", description="Access the endpoint with the URL key to be redirected to the target URL.")
def forward_to_url(
    url_key:str,
    request: Request,
    db: Session = Depends(get_db)
    ):

    db_url = crud.get_db_url_by_key(db=db, url_key=url_key) #db URL receives the URL object that matches the key and is active, or None if no match is found
    if db_url:
        db_url.clicks += 1 #increments the clicks attribute of the URL object
        db.commit() #updates the database with the new clicks value
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.post("/unuse/{secret_key}", description="Sets the is_active attribute of the URL object that matches the secret key to False, making it inactive.")
def admin_unuse_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_secret_key(db=db, secret_key=secret_key)
    if not db_url:
        raise_not_found(request)
    db_url.is_active = False
    db.commit()
    return {"message": f"URL with key '{db_url.key}' is now inactive"}



@app.delete("/url/{secret_key}", description="Deletes the URL object from the database that matches the secret key.")
def admin_delete_url(secret_key: str, request = Request, db: Session = Depends(get_db)):
    if not crud.get_db_url_by_secret_key(db=db, secret_key=secret_key):
        raise_not_found(request)

    url_key = crud.get_db_url_by_secret_key(db=db, secret_key=secret_key).key    
    crud.delete_db_url(db=db, url_key=url_key)
    return {"message": f"URL with key '{url_key}' deleted successfully"}



@app.post("/url", response_model=URL_info, description="Creates a new URL object in the database and returns it.") #response model is the model that will be returned to the user
def create_url(url: schemas.URL_base, db: Session = Depends(get_db)):
    if not validators.url(url.target_url): #checks if its a valid URL
        return raise_bad_request(message="URL not valid")
    
    db_url = crud.create_db_url(db=db, url=url) #creates the URL in the database, updates the database and returns the URL object
    db_url.url = db_url.key 
    db_url.admin_url = db_url.secret_key
    
    return db_url

