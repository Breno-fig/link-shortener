import secrets, string
from . import crud
from sqlalchemy.orm import Session

def create_random_key(length: int) -> str: #arrow indicates the return type of the function
    chars = string.ascii_uppercase + string.digits  #key can have uppercase letters and numbers
    return "".join(secrets.choice(chars) for _ in range(length)) 

def create_unique_key(db: Session, length: int = 5) -> str:
    key = create_random_key(length)
    while crud.get_db_url_by_key(db, key): #checks if theres an URL with that key
        key = create_random_key(length) #if there is, it generates a new key until it finds one that is unique
    return key
