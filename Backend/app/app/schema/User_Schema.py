from pydantic import BaseModel, EmailStr, Field


class UserInfo(BaseModel):
    username: str 
    first_name:str
    last_name: str
    email: EmailStr
    phone:str
    password: str
                          
    role_id:int = 1
    is_active:bool = True


class Update_User(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    phone: str = Field(max_digits= 10)
    role_id:str = Field(example="Admin/User")
    profile_pic_URL:str  

class UserLogin(BaseModel):
    username_or_email: str
    password: str = Field(min_length=3)


class UserVerify(BaseModel):
    otp: int
    resetkey: str


class OTPVerify(BaseModel):
    resetkey: str
    otp: int


class ForgotPass(BaseModel):
    email: EmailStr


class ResetPass(BaseModel):
    resetkey: str
    new_password: str = Field(min_length=3)


class ChangePass(BaseModel):
    Current_Password: str
    New_Password: str = Field(min_length=6)
    Confirm_Password: str = Field(min_length=6)


class resend_otp(BaseModel):
    reset_key: str





'''from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserInfo(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(pattern=r'^\d{10}$')  # 10 digit phone number

    password: str = Field(
        min_length=6,
        pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$'
    )

    role_id: int = 1
    is_active: bool = True


class Update_User(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(pattern=r'^\d{10}$')
    role_id: str = Field(example="Admin/User")
    profile_pic_URL: str | None = None


class UserLogin(BaseModel):
    username_or_email: str
    password: str = Field(min_length=6)


class UserVerify(BaseModel):
    otp: int = Field(ge=100000, le=999999)  # 6 digit OTP
    resetkey: str


class OTPVerify(BaseModel):
    resetkey: str
    otp: int = Field(ge=100000, le=999999)


class ForgotPass(BaseModel):
    email: EmailStr


class ResetPass(BaseModel):
    resetkey: str
    new_password: str = Field(
        min_length=6,
        pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$'
    )


class ChangePass(BaseModel):
    Current_Password: str

    New_Password: str = Field(
        min_length=6,
        pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$'
    )

    Confirm_Password: str

    @field_validator("Confirm_Password")
    def password_match(cls, v, info):
        if "New_Password" in info.data and v != info.data["New_Password"]:
            raise ValueError("Passwords do not match")
        return v


class resend_otp(BaseModel):
    reset_key: str'''