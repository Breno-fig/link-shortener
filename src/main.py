from src.schemas.schemas import URL_conf

import validators
from fastapi import FastAPI, HTTPException

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/url")
def create_url(url: URL_conf):
    if not validators.url(url.target_url): #checks if its a valid URL
        return raise_bad_request(message="URL not valid")
    return {"TODO: create dabase entry for": url.target_url} 
    