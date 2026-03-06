from pydantic import BaseModel,EmailStr

class User(BaseModel):
    username: str
    first_name:str
    last_name: str
    email: EmailStr
    phone:int
    password:str
    role_id:int
    is_active:bool

class Update_User(BaseModel):
    username: str
    first_name:str
    last_name: str
    email: EmailStr
    phone:int
    role_id:int
    profile_pic_URL:str
    Is_two_fath:bool   

class UserLogin(BaseModel):
    username_or_email:str
    password:str

class UserVerify(BaseModel):
    otp: str
    token: str

class OTPVerify(BaseModel):
    email: str
    otp: int
    token : str
    
class ForgotPass(BaseModel):
    email:EmailStr

class ResetPass(BaseModel):
    new_password:str

class ChangePass(BaseModel):
    email:EmailStr
    Current_Password:str
    New_Password:str
    Confirm_Password:str