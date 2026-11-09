from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str 
    batch: int 
    price: float
    description: str | None = None

items : List[Item] = [] 


@app.post("/items")
def demo_create(item: Item):
    items.append(item)
    print(f"item")
    return item

@app.get("/items")
def demo_show():
    return items


@app.delete("/items/{item_batch}")
def demo_delete(item_batch: int):
    for i in range(len(items)):
        if items[i].batch == item_batch:
            deleted_item = items.pop(i)
            return {"message": "Item deleted", "item": deleted_item}




