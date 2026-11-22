from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import auth
from app.database import get_db
from app.models import User
from app.utils.secure import verify_password
from app.services.oauth2 import create_access_token


router = APIRouter(prefix='/auth', tags=['Authentication'])




@router.post('/login', response_model=auth.Token)
def login(user_login : OAuth2PasswordRequestForm = Depends(),
          db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user_login.username).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid email!")

    if not verify_password(user_login.password, existing_user.password):

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid password !")

    access_token = create_access_token(data={"user_id" : existing_user.id})
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }