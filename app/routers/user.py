from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import user


router = APIRouter(prefix="/user",
                   tags=['User API'])


@router.get('/', response_model=list[user.UserResponse])
def get_users(db : Session = Depends(get_db)):

    all_users = db.query(User).all()

    if all_users is None:

        return {
            "message" : "No user found"
        }

    return all_users



@router.get('/{id}')
def get_user():
    pass

@router.post('/')
def create_user(user_data : user.UserBase,
                db : Session = Depends(get_db)):

    new_user = User(**user_data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message" : "user created ",
        "user" : new_user
    }

@router.put('/{id}')
def update_user():
    pass

@router.delete('/{id}')
def delete_user():
    pass