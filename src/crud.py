from sqlalchemy.orm import Session

from . import keygen, models, schemas

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    ) #returns the first URL object that matches the key and is active, or None if no match is found

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key)
        .first()
    ) #returns the first URL object that matches the secret key and is active, or None if no match is found


def create_db_url(db: Session, url: schemas.URL) -> models.URL:
    key = keygen.create_unique_key(db)
    secret_key = keygen.create_unique_key(db, length=8)
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def delete_db_url(db: Session, url_key: str) -> None:
    db_url = get_db_url_by_key(db, url_key)
    if db_url:
        db.delete(db_url)
        db.commit()