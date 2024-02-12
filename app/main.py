from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional,List
import psycopg2

from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user,auth




models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    




    

   
    
    
try:
    conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='123',cursor_factory=psycopg2.extras.RealDictCursor)
    cursor=conn.cursor()
    print("database connection successfully!")
except Exception as error:
    print("connecting database failed")
    print("error",error)  
    
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)        

@app.get("/")
async def root():
    return {"data": "Hello World1"}


@app.get("/getsqlalchemy")
def test_post(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data": posts}


###############
