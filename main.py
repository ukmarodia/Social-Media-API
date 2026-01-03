from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str 
    content:str
    published: bool = True
    rating: Optional[int] = None 

my_posts = [{"title":"title of post1", "content":"content of post1", "id": 1},{"title": "Favourite foods", "content":"I like pizza", "id":2}]

@app.get("/")
async def root():
    return {"message": "Hello WOrld"}

@app.get("/posts")
def get_post():
    return {"Data": my_posts}

@app.post("/posts")
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}