from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import auth
from app.database import get_db
from app.models import User
from app.utils.secure import verify_password


router = APIRouter(prefix='/auth', tags=['Authentication'])




@router.post('/login')
def login(login : auth.LoginBase,
          db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == login.email).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid email!")

    if not verify_password(login.password, existing_user.password):

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid password !")

    return {
        "message" : "login success"
    }