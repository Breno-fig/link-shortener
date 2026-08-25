from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

Fake_Items_DB = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(str, Enum):
    breno = "breno"
    adriel = "adriel"
    alan = "alan"


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None, short: bool = False): #| None = None means that the parameter is optional
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/files/{file_path:path}")
def read_file(file_path:str):
    return {"file_path": file_path}

@app.get("/items/fake_items/")
async def read_fake_items(skip: int = 0, limit: int = 10):
    return Fake_Items_DB[skip : skip + limit]










# @app.get("/usr/{model_name}")
# def get_model(model_name: ModelName):
#     if model_name is ModelName.breno:
#         return {"model_name": model_name, "message": "Breno Lindo!"}
    
#     if model_name.value == "adriel":
#         return {"model_name": model_name, "message": "ola! Adriel"}

#     if model_name.value == ModelName.alan:
#         return {"model_name": model_name, "message": "Ola! Alan"}
    
#     return {"model_name": model_name, "message": "voce eh merda!"}
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}