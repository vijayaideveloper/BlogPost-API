from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Post
from app import schemas
from app.services.oauth2 import get_current_user



router = APIRouter(prefix="/posts",
                   tags=['Post API'])

# ---------------- GET ALL POSTS ----------------

@router.get(
    "/",
    response_model=list[schemas.PostResponse],
)
def get_posts(db: Session = Depends(get_db),
              current_user : int = Depends(get_current_user)):
    
    return db.query(Post).filter(Post.user_id==current_user.id).all()


# ---------------- GET SINGLE POST ----------------

@router.get(
    "/{post_id}",
    response_model=schemas.PostResponse,
)
def get_post(post_id: int, 
             current_user : int = Depends(get_current_user),
             db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.user_id == current_user.id).filter(Post.id==post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    return post


# ---------------- CREATE POST ----------------

@router.post("/",
    response_model=schemas.PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db),
                current_user : int = Depends(get_current_user)):

    new_post = Post(user_id=current_user.id, **post.model_dump())

    try:

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create the post."
        )

    
# ---------------- UPDATE POST ----------------

@router.put("/{post_id}",
            response_model=schemas.PostResponse
)
def update_post(
    post_id: int,
    post: schemas.PostBase,
    current_user : int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_post = db.query(Post).filter(
        Post.user_id == current_user.id
    ).filter(Post.id==post_id).first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    try:
        post_data = post.model_dump()

        for key, value in post_data.items():
            setattr(existing_post, key, value)

        db.commit()
        db.refresh(existing_post)

        return existing_post

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update the post."
        )


# ---------------- DELETE POST ----------------

@router.delete("/{post_id}",)
def delete_post(
    post_id: int,
    current_user : int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_post = db.query(Post).filter(
            Post.user_id == current_user.id
        ).filter(Post.id==post_id).first()

    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    try:
        db.delete(existing_post)
        db.commit()

        return {
            "message": "Post deleted successfully"
        }

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete the post."
        )


