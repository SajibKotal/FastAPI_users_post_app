from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=False
    
class PostCreate(PostBase):
    pass

   
class Post(PostBase):
    id:int
    created_at:datetime
    class Config:
        orm_mode=True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
        

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True                


class UserLogin(BaseModel):
    email: EmailStr
    password: str           
    
class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None    
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None    