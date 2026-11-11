#install jwt library through pip install python-jose
from fastapi import FastAPI, HTTPException, Depends
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
    print(token)
    return token


# my_data = {
#     "name":"Hamza"
# }
# create_token(my_data)


