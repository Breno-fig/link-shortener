from pydantic import BaseModel

class URL_base(BaseModel): 
    target_url: str

class URL(URL_base):
    is_active: bool
    clicks: int

    class Config:
        from_attributes = True

class URL_info(URL):
    url: str
    admin_url: str

