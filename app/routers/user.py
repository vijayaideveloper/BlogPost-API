from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app import schemas
from app.utils.secure import hash_password

router = APIRouter(prefix="/user",
                   tags=['User API'])


@router.get('/', response_model=list[schemas.UserResponse])
def get_users(db : Session = Depends(get_db)):

    all_users = db.query(User).all()

    if all_users is None:

        return {
            "message" : "No user found"
        }

    return all_users



@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id : int,
             db : Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no user found in this id {id}')

    return existing_user

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user_data : schemas.UserBase,
                db : Session = Depends(get_db)):
    
    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message" : "user created ",
        "user" : new_user
    }


@router.put('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_202_ACCEPTED)
def update_user(id : int,
                user_data : schemas.UserBase,
                db : Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'no user found in this id {id}')
    
    hashed_password = hash_password(user_data.password)
    
    existing_user.email = user_data.email
    existing_user.password = hashed_password

    db.commit()
    db.refresh(existing_user)

    return existing_user


@router.delete('/{id}')
def delete_user(id : int,
             db : Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.id == id).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no user found in this id {id}')

    db.delete(existing_user)
    db.commit()

    return {
        "message" : "deleted",
        "user" : existing_user
    }