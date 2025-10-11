from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Normal Endpoint
@app.get("/")
def read_root():
    return {"message" : "Hello from Dublin"}


# Params
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# Query
@app.get("/search")
def search_item(q: str = None, limit: int = 10):
    return {"query": q, "limitdaflsh": limit}

# Movies
@app.get("/movies")
def movies(name: str = None, actor: str = None, Year: int = 2001):
    return {"movie name": name, "Actor": actor, "year": Year}

# Travel
@app.get("/travel")
def travel(countries: str = None, city: str = None, distance: int = 500):
    return {"country name": countries, "city name": city, "countries distance": distance}

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items")
def create_item(item: Item):
    return {"item": item}
