from fastapi import FastAPI

from . import models
from .api.main import api_router
from .core.db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
