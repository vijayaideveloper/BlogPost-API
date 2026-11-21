from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Post
from app.schemas.post import CreatePost, PostResponse



router = APIRouter(prefix="/posts",
                   tags=['Post API'])

# ---------------- GET ALL POSTS ----------------

@router.get(
    "/",
    response_model=list[PostResponse],
)
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.id.desc()).all()


# ---------------- GET SINGLE POST ----------------

@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    return post


# ---------------- CREATE POST ----------------

@router.post("/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: CreatePost, db: Session = Depends(get_db)):

    new_post = Post(**post.model_dump())

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
            response_model=PostResponse
)
def update_post(
    post_id: int,
    post: CreatePost,
    db: Session = Depends(get_db)
):

    existing_post = db.query(Post).filter(
        Post.id == post_id
    ).first()

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
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found."
        )

    try:
        db.delete(post)
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


