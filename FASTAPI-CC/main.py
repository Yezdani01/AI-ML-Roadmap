from fastapi import FastAPI #fasttttt apiii!!!
from typing import List #kya hai ki T..T
from model.model import Thing

app = FastAPI()
things : List[Thing] = []

@app.get("/")
def read():
    return {"message":"Nobody is here"}


@app.get("/things")
def get_things():
    return things


@app.post("/things")
def add_thing(thing: Thing):
    things.append(thing)
    return thing

@app.put("/things/{thing_id}")
def update_thing(thing_id: int,updated_thing: Thing):
    for index,thing in enumerate(things):
        if thing.id == thing_id:
            things[index]=updated_thing
            return updated_thing
    return {"Error":"Thing not found"}       

@app.delete("/things/{thing_id}")
def delete_thing(thing_id: int):
    for index,thing in enumerate(things):
        if thing.id == thing_id:
            deleted = things.pop(index)
            return deleted

    return {"Error":"Thing not found"}

    