from fastapi import FastAPI, Header
from typing import Annotated

app = FastAPI()

@app.get("/users")
async def get_users(user_agent: Annotated[str | None,Header()] = None):
    return user_agent