from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI,Depends,HTTPException

# for the sql alchemy
from sqlalchemy import create_engine ,Column, Integer, String
from sqlalchemy.orm import declarative_base,Session,sessionmaker #object relational mapping

#for the password hashing python-jose[cryptography] passlib bcrypt==4.0.1 python-multipart
from passlib.context import CryptContext

#jwt imports
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

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
    hashed_password = Column(String,nullable=False)

Base.metadata.create_all(bind=engine)

def check_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    points: int
    password: str

class UserResponse(BaseModel):
    username: str
    email: str
    points: int

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    points: int | None = None

class Loginrequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

#for the password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#for the jwt 
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


def create_token(data:dict,expires_delta: timedelta,token_type:str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp":expire,
        "type": token_type
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token


# -------------API---------------



@app.post("/refresh")
def refresh_access_token(
    refresh_data: RefreshRequest,
    db: Session = Depends(check_db)
):
    # 1. Decode and verify the refresh token
    payload = jwt.decode(
    refresh_data.refresh_token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
)
    token_type = payload.get("type")

    # 2. Extract username from the payload using "sub"
    username = payload.get("sub")
    # 3. Check whether token type is "refresh"
    # 4. If invalid or expired, raise HTTP 401
    if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 5. Check whether the user still exists in the database
    user = db.query(User).filter(User.id == username).first()
    if not user:
        raise HTTPException(status_code=404,detail="User does not exists")

    # 6. Generate a NEW access token
    token = create_token(
        {
            "sub":username
        },
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="refresh"
    )
    # 7. Return the new access token
    return {
        "access_token":token
    }

@app.post("/login")
def login(user: Loginrequest, db: Session = Depends(check_db)):
    # 1. Find the user by username
    data = db.query(User).filter(User.username == user.username).first()
    # 2. If user doesn't exist, raise HTTP 401
    if not data:
        raise HTTPException(status_code=401,detail="The user not found")
    # 3. Verify entered password against hashed password
    # 4. If password is incorrect, raise HTTP 401
    if verify_password(user.password, data.hashed_password) == False:
            raise HTTPException(status_code=401,detail="username or password is incorrect")
    # 5. Generate access token
    access_token = create_token(
    {
        "sub": user.username
    },
    timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    "access"
    )
    # 6. Generate refresh token
    refresh_token = create_token(
        {
            "sub":user.username
        },
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh"
    )
    # 7. Return both tokens and token type
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
    }




@app.post("/register")
def register_user(user:UserCreate,db: Session = Depends(check_db)):
    data = db.query(User).filter(User.username == user.username).first()
    if data:
        raise HTTPException(status_code=404,detail=f"The user {user.username} exists")
    else:
        # data = User(
        #     username=user.username,
        #     email=user.email,
        #     points=user.points,
        #     hashed_password=hash_password(user.password)
        # )
        user_data = user.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))
        # What does pop("password") do?
        # - Retrieves the password.
        # - Removes the password key from the dictionary.
        # - We then store its hash under hashed_password.
        data = User(**user_data)

        db.add(data)
        db.commit()
        db.refresh(data)
    return {
        "Data":{f"Added the {user.username} data successfully"}
    }

@app.post("/users",response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(check_db)):

    data = User(username = user.username,
                email = user.email,
                points = user.points,
                hashed_password = hash_password(user.password)
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