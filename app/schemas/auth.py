from pydantic import BaseModel, EmailStr


class LoginBase(BaseModel):

    email : EmailStr
    password : str