from typing import List, Optional
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException , Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import PostCreate , PostBase , Post, PostOut
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/" , response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 10, skip: int = 0, search: Optional[str] = ""): #db: session and all makes it a dependency
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    print(limit)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #db: session and all makes it a dependency

    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)

    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) #unpacking the dictionary -eliminates the need to write the column names manually
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # basically stores the new post in the database and stores it in the new_post variable



    return new_post # sends back a dictionary


@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    #we are removing this functionality because we want all te posts to be public
    
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail=f"Not authorized to perform requested action")
    
    return post

    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}" , response_model=Post)
def update_post(id:int, post: PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *""", (post.title, post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    updated_post.update(post.model_dump(), synchronize_session= False)
    db.commit()
    
    return updated_post.first()
