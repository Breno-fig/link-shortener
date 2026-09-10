import validators
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ... import crud, schemas
from ..deps import get_db


router = APIRouter()


def raise_bad_request(message: str) -> None:
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request: Request) -> None:
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@router.get(
    "/{url_key}",
    description="Access the endpoint with the URL key to be redirected to the target URL.",
)
def forward_to_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        db_url.clicks += 1
        db.commit()
        return RedirectResponse(db_url.target_url)
    raise_not_found(request)


@router.post(
    "/url",
    response_model=schemas.URL_info,
    description="Creates a new URL object in the database and returns it.",
)
def shorten_url(url: schemas.URL_base, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        return raise_bad_request(message="URL not valid")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return db_url


@router.post(
    "/unuse/{secret_key}",
    description="Sets the is_active attribute of the URL to False, if it exists",
)
def admin_unuse_url(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    db_url = crud.get_db_url_by_secret_key(db=db, secret_key=secret_key)
    if not db_url:
        raise_not_found(request)
    db_url.is_active = False
    db.commit()
    return {"message": f"URL with key '{db_url.key}' is now inactive"}


@router.post(
    "/reuse/{secret_key}",
    description="Sets the is_active attribute of the URL to True, if it exists",
)
def admin_reuse_url(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    db_url = crud.get_db_url_by_secret_key(db=db, secret_key=secret_key)
    if not db_url:
        raise_not_found(request)
    db_url.is_active = True
    db.commit()
    return {"message": f"URL with key '{db_url.key}' is now active"}


@router.delete(
    "/url/{secret_key}",
    description="Deletes the URL object from the database",
)
def admin_delete_url(
    secret_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    url = crud.get_db_url_by_secret_key(db=db, secret_key=secret_key)
    if not url:
        raise_not_found(request)
    crud.delete_db_url(db=db, url_key=url.key)
    return {"message": f"URL with key '{url.key}' deleted successfully"}
