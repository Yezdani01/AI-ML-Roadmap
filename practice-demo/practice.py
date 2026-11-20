from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    points: int

user = User(
    username = "Hamza",
    email = "hamza@gmail.com",
    points = 50
)

print(user)
print(user.username)
print(user.points)

