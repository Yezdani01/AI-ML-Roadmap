from fastapi import FastAPI, Request
from typing import Union
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = FastAPI()



# db_url = os.getenv("database_access")

conn = MongoClient("mongodb+srv://yezdanihamza_db_user:VdkSNwlwUohb3fCB@hamza-cluster.ihlxytu.mongodb.net")






# @app.get("/items/{items_id}")
# def read_item(item_id: int, q: Union[str, None] = None):    
#     return {"item_id": item_id, "q": q}