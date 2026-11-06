from pydantic import BaseModel #validation

class Thing(BaseModel):
    id: int
    name: str
    origin: str




