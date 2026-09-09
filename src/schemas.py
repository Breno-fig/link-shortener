from pydantic import BaseModel, ConfigDict

class URL_base(BaseModel): 
    target_url: str

class URL(URL_base):
    is_active: bool
    clicks: int

    model_config = ConfigDict(from_attributes=True) #tells pydantic to read the attributes from the SQLAlchemy model, instead of reading them from the request body

class URL_info(URL):
    url: str
    admin_url: str

