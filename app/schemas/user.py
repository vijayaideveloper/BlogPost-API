
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr



class UserBase(BaseModel):

    email : EmailStr
    password : str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at : datetime
    
