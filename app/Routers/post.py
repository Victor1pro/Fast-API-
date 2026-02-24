from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.schemas.user import PostCreate, PostResponse, PostVote
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models.user import Post, Vote
from typing import List, Optional
from app.utils.oauth2 import get_current_user

# Create a Route
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Get Posts (RAW SQL)
# @app.get("/posts") 
# def get_posts(): 
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     cursor.execute("""SELECT * FROM posts""") 
#     rows = cursor.fetchall() 
#     posts = [dict(row) for row in rows] 
#     return {"data": posts}


# Get Posts (ORM VERSION)
@router.get("/", response_model=List[PostVote])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    Limit: int = 10,
    Skip: int = 0,
    Search: Optional[str] = ""
):
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .filter(Post.title.contains(Search))
        .group_by(Post.id)
        .limit(Limit)
        .offset(Skip)
        .all()
    )

    response = [
        {
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "post": post,
            "votes": votes
        }
        for post, votes in posts
    ]
    return response


# Get latest Post (RAW SQL VERSION)
# @app.get("/posts/latest") 
# def get_latest_post(): 
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""") 
#     row = cursor.fetchone() 
#     if not row: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found") 
#     return {"latest_post": dict(row)}


# Get latest Post (ORM VERSION)
@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post).order_by(Post.id.desc()).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested Action")

    return post


# Get Single Post (RAW SQL)
# @app.get("/posts/{id}") 
# def get_post(id: int): 
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     cursor.execute("""SELECT * FROM posts WHERE id = ?""", (id),) 
#     row = cursor.fetchone() 
#     if not row: 
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found" ) 
#     post = dict(row) # Convert sqlite3.Row → dict 
#     return {"post": post}


# Get Single Post (ORM VERSION)
@router.get("/{id}", response_model=PostVote) 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): 

    post = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found") 
    return post


# Create a post (RAW SQL)
# @app.post("/posts", status_code=status.HTTP_201_CREATED) 
# def create_posts(post: Post): 
#     #####      RAW SQL      #####
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (?, ?, ?) RETURNING *""", (post.title, post.content, post.published) ) 
#     row = cursor.fetchone() 
#     conn.commit() 
#     return {"data": dict(row)}


# Create a Post (ORM VERSION)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): 
    new_post = Post(owner_id = current_user.id, title = post.title, content = post.content, published = post.published)
    # new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Delete a Post (RAW SQL)
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
# def delete_post(id: int): 
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     cursor.execute("""DELETE FROM posts WHERE id = ? RETURNING *""", (id,)) 
#     row = cursor.fetchone() 
#     if not row: 
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist" ) 
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# Delete a Post (ORM VERSION)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): 
    post = db.query(Post).filter(Post.id == id).first() 
    if not post: 
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist" ) 
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested Action")
    
    db.delete(post) 
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post (RAW SQL)
# @app.put("/posts/{id}") 
# def update_post(id: int, post: Post): 
#     conn = connect_to_db() 
#     cursor = conn.cursor() 
#     try:
#         cursor.execute(""" UPDATE posts SET title = ?, content = ?, published = ? WHERE id = ? RETURNING * """, (post.title, post.content, post.published, id) ) 
#         row = cursor.fetchone() 

#         if not row: 
#             raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist" ) 
#         conn.commit() 
#         return {"updated_post": dict(row)}
#     except Exception as error:
#         conn.rollback()
#         raise error
#     finally:
#         conn.close()


# Update a Post (ORM VERSION)
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    existing_post = post_query.first()

    if existing_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} does not exist"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested Action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()