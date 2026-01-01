from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str 
    content:str
    published: bool = True
    rating: Optional[int] = None 

@app.get("/")
async def root():
    return {"message": "Hello WOrld"}

@app.get("/getPost")
def get_post():
    return {"Data": "this is your posts"}

@app.post("/createpost")
def create_post(new_post: Post):
    print(new_post.rating)
    return {"data":"new Post"}