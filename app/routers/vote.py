from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.services import oauth2
from app.database import get_db
from app import schemas
from app.models import Vote, Post



router = APIRouter(prefix="/vote",
                   tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote,
         db : Session = Depends(get_db),
         current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(Post).filter(Post.id==vote.post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {vote.post_id} is not found"
        )

    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id==current_user.id)
    found_vote = vote_query.first()

    if (vote.dir==1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
                )
        
        new_vote = Vote(
            post_id=vote.post_id,
            user_id=current_user.id
        )

        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return {
            "message" : "successfully added vote"
        }

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {
                    "message" : "successfully deleted vote"
                }