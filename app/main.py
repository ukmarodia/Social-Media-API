from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app import models


from app.database import  engine, get_db
models.Base.metadata.create_all(bind=engine)
app = FastAPI()





class Post(BaseModel):
    title: str 
    content:str
    published: bool = True
while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', port = "5433", user='postgres', password='umang', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)






@app.get("/")
async def root():
    return {"message": "Hello WOrld"}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    
    return {"Data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(new_post.title, new_post.content, new_post.published))
    # mpost = cursor.fetchone()
    # conn.commit()
    
    mpost =models.Post(**new_post.dict())
    db.add(mpost)
    db.commit()
    db.refresh(mpost)
    return {"data": mpost}




@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id))) 
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id== id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": "Post not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,(str(id))))
    # update = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posty = post_query.first()
    if posty == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"index {id} not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    
   

    
     
    
    return {"data": post_query.first()}
    