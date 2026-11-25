from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.typing import conint


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    published: bool = True



class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    user_id : int


class UserBase(BaseModel):

    email : EmailStr
    password : str


class UserResponse(UserBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at : datetime


class LoginBase(BaseModel):

    email : EmailStr
    password : str


class Token(BaseModel):

    access_token : str
    token_type : str

class TokenData(BaseModel):

    id : Optional[int] = None


class Vote(BaseModel):

    post_id : int
    dir : int