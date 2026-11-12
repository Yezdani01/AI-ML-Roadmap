#I am main.py and I am here.

from fastapi import FastAPI, HTTPException, Depends, Header#we dont need header as its work will be done through the oauth2,
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

app = FastAPI()


#JWT CONFIG
SECRET_KEY = "SECRET"
ALGORITHM = "HS256" #encryption algorithm for small applications
#HS512.- has a secret key and strong hashing 
#RS256 - has public and private key and used in prod
#ES256 - high crypto method and high secure 
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#PASSWORD HASHING SETUP
pwd_context = CryptContext(schmes=["bycrypt"])
#we are using the bcrypt here

#Oauthsetup
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#Dummy user DB for our convenience
user_db = {
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}

#hash_password
def hash_password(password: str):
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#create the token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update(
        {
            "exp":expire
        }
    )
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    # print(token)
    return token


# my_data = {
#     "name":"Hamza"
# }
# create_token(my_data)

#login(through the oaith 2 form)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get(form_data.username)
    if not user or not verify_password:
        raise HTTPException(status_code=400,detail="invalid username or password")
    access_token = create_token(
        {
            "sub":form_data.username
            }
            )

    return{
        "Access_token":access_token,
        "Token Type":"bearer"
    }
    

#verify the credentials broo.
def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401,detail="Invalid or Expired Token")


#protected route
@app.get("/secure")
def secure_data(user = Depends(verify_token)):
    return{
        "message":"Secure Data accessed",
        "user":user
    }
