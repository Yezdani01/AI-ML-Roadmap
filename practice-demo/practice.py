from pydantic import BaseModel, Field
from fastapi import FastAPI


app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str
    points: int
    address: str | None = None

class UserResponse(BaseModel):
    username: str
    email: str
    points: int

user = UserCreate(
    username = "Hamza",
    email = "hamza@gmail.com",
    points = 50
)

# print(user)
# print(user.username)
# print(user.points)


@app.get("/")
def get_endpoint():
    return {
        "message":"Hii! Welcome Back!"
    }

@app.post("/users")
def post_users(user: UserResponse):
    return {
        "message":"Done successfully",
        "user":user
    }


