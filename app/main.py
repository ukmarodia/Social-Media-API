from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import schema
from app import models, utils
from .routers import post, user 

from app.database import  engine, get_db



models.Base.metadata.create_all(bind=engine)
app = FastAPI()






# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', port = "5433", user='postgres', password='umang', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)



@app.get("/")
async def root():
    return {"message": "Hello WOrld"}
