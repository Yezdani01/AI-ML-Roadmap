from pydantic import BaseModel, Field
from fastapi import FastAPI,Depends,HTTPException

# for the sql alchemy
from sqlalchemy import create_engine ,Column, Integer, String
from sqlalchemy.orm import declarative_base,Session,sessionmaker #object relational mapping

app = FastAPI()


#using the SQLALCHEMY 
Base = declarative_base()


DATABASE_URL = "sqlite:///./test.db" #using the sqlite
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
sessionlocal = sessionmaker(bind = engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    points = Column(Integer)

Base.metadata.create_all(bind=engine)

def check_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()



class UserCreate(BaseModel):
    username: str
    email: str
    points: int
    address: str | None = None

class UserResponse(BaseModel):
    username: str
    email: str
    points: int

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    points: int | None = None


user = UserCreate(
    username = "Hamza",
    email = "hamza@gmail.com",
    points = 50
)

# print(user)
# print(user.username)
# print(user.points)



# -------------API---------------

@app.post("/users",response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(check_db)):

    data = User(username = user.username,
                email = user.email,
                points = user.points,
                )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data
    

@app.get("/users")
def get_users(db: Session = Depends(check_db)):
    data = db.query(User).all()
    return{
            "Total":len(data),
            "Data":data
        }


#to get a specific user data

@app.get("/users/{user_id}")
def get_user(user_id: int,db: Session = Depends(check_db)):
    data = db.query(User).filter(User.id == user_id).first()
    if not data:
        raise HTTPException(status_code=404,detail="User not found")

    return {"data":data}


@app.put("/users/{user_id}")
def update_user(user_id: int,updated_user: UserCreate,db: Session = Depends(check_db)):
    data = db.query(User).filter(User.id == user_id).first()
    if not data:
        raise HTTPException(status_code=404,detail="User not found")

    data.username = updated_user.username #type: ignore
    data.email = updated_user.email#type: ignore
    data.points = updated_user.points#type: ignore

    db.commit()
    db.refresh(data)
    return {
        "data":data
    }

@app.patch("/users/{user_id}")
def patch_user(user_id : int, updated_user: UserUpdate, db: Session = Depends(check_db)):
    data = db.query(User).filter(User.id == user_id).first()

    if not data:
        raise HTTPException(status_code=404,detail="User not found")

    if updated_user.username is not None:
        data.username = updated_user.username #type: ignore
    if updated_user.email is not None:
        data.email = updated_user.email#type: ignore
    if updated_user.points is not None:
        data.points = updated_user.points#type: ignore


    db.commit()
    db.refresh(data)

    return {
        "data":data
    }

@app.delete("/users/{user_id}")
def delete_user(user_id:int,db: Session = Depends(check_db)):
    data = db.query(User).filter(User.id == user_id).first()

    if not data:
        raise HTTPException(status_code=404,detail="Data not found")
    db.delete(data)
    db.commit()

    return {
        "Deleted":f"Successfully deleted the {data.username}'s data"
    }