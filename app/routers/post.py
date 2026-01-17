from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schema, models
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(
    prefix="/post",
    tags=['Post']
)



@router.get("/", response_model = List[schema.Post])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    
    return  posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schema.Post)
def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(new_post.title, new_post.content, new_post.published))
    # mpost = cursor.fetchone()
    # conn.commit()
    
    mpost =models.Post(**new_post.dict())
    db.add(mpost)
    db.commit()
    db.refresh(mpost)
    return mpost




@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id))) 
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id== id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": "Post not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)),)
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,(str(id))))
    # update = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posty = post_query.first()
    if posty == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"index {id} not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    
   

    
     
    
    return  post_query.first()