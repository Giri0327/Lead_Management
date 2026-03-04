from pydantic import BaseModel

class User(BaseModel):
    username: str
    first_name:str
    last_name: str
    email: str
    phone:int
    profile_pic:str
    password:str

class UserLogin(BaseModel):
    username_or_email:str
    password:str

class UserVerify(BaseModel):
    otp: str
    token: str



