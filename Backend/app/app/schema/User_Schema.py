from pydantic import BaseModel,EmailStr,Field,ConfigDict


class UserInfo(BaseModel):
    username: str
    first_name:str
    last_name: str
    email: EmailStr
    phone:str
    password: str = Field(min_length=6)
    role_id:int
    is_active:bool


class Update_User(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    phone: str
    role_id:str = Field(example="Admin/User")
    profile_pic_URL:str  

class UserLogin(BaseModel):
    username_or_email:str
    password: str = Field(min_length=6)


class UserVerify(BaseModel):
    otp: int 
    resetkey: str

class OTPVerify(BaseModel):
    resetkey : str
    otp: int


class ForgotPass(BaseModel):
    email:EmailStr

class ResetPass(BaseModel):
    otp : int 
    resetkey : str 
    new_password:str = Field(min_length=6)

class ChangePass(BaseModel):
    Current_Password:str 
    New_Password:str = Field(min_length=6)
    Confirm_Password:str = Field(min_length=6)


class resend_otp(BaseModel):
    reset_key : str
