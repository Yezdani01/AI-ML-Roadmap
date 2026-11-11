#install jwt library through pip install python-jose
from fastapi import FastAPI, HTTPException, Depends, Header
from jose import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI()

SECRET_KEY = "SECRET"

ALGORITHM = "HS256" #encryption algorithm for small applications

#HS512.- has a secret key and strong hashing 
#RS256 - has public and private key and used in prod
#ES256 - high crypto method and high secure 



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

#login
@app.post("/login")
def login(username: str, password: str):
    if username != "admin" or password != "1234":
        raise HTTPException(status_code=401,detail="Invalid Username or password" )
    
    token = create_token({
        "sub":username
    })
    return{
        "accesstoken":token
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
