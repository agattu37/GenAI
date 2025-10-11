from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# command to run and bring up the server = uvicorn basic_mod:app --reload

# Normal Endpoint
@app.get("/")
def read_root():
    return {"message" : "Hello from FastAPI"}


# pass Params after items
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# a Search route for Query
@app.get("/search")
def search_item(q: str = None, limit: int = 12):
    return {"query": q, "Hockey Score": limit}

# a Base class
class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)
    price: float = Field(..., ge=0, le=100)
    description: str | None = None

# return the items base structure
@app.post("/items")
def create_item(item: Item):
    return {"item": item}

# return the item id along the item structure
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id}
