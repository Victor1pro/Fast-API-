from fastapi import FastAPI, APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Votes
from app.models.user import Vote, Post
from app.database import get_db
from app.utils.oauth2 import get_current_user


router = APIRouter(
    tags=["User Vote"],
    prefix="/vote"
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Votes, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")


    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Succesfully added Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not Exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message": "Successfully deleted Vote"}
        

