from pydantic import BaseModel

class URL_base(BaseModel):
    target_url: str

class URL(URL_base):
    active: bool
    access: int

    class Config:
        from_attributes = True

class URL_conf(URL):
    url: str
    admin_url: str

