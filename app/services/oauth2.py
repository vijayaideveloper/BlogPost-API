from jose import JWSError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from app.schemas import auth
import os
from dotenv import load_dotenv

Oauth_Scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()

SECURE_KEY = os.getenv("SECURE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_MINUTES = os.getenv("ACCESS_TOKEN_MINUTES")


def create_access_token(data : dict, key=SECURE_KEY, algorithm=ALGORITHM):

    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_MINUTES))
    encode_data.update({"expire" : expire.timestamp()})

    encoded_jwt = jwt.encode(encode_data, key, algorithm=algorithm)

    return encoded_jwt

def verify_access_token(token : str, credentials_exception):

    try:
        payload = jwt.decode(token, key=SECURE_KEY, algorithms=ALGORITHM)

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = auth.TokenData(id=id)

    except JWSError:

        raise credentials_exception

    return token_data

def get_current_user(token : str = Depends(Oauth_Scheme)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Not a valid credentials",
                                          headers={"WWW-Authenticate" : "Bearer"})

    return verify_access_token(token, credentials_exception)