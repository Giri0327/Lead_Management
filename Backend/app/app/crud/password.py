from app.schema import *
from sqlalchemy.orm import Session
from app.models import *
from app.db import *
import random
from datetime import datetime,timedelta
from app.core import pwd_context,verify_password
from app.core import emailOTP
from fastapi import HTTPException,status



def forgot_password(user:ForgotPass,db:Session):

    dbuser = db.query(User).filter(User.Email==user.email).first()

    if not dbuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not Found!")
    else:
        otp=random.randint(100000,999999)
        print("OTP:",otp)
        expiry=(datetime.now()+timedelta(minutes=10))
        dbuser.OTP = otp
        dbuser.OTP_Expiry = expiry
        db.commit()

        emailOTP(dbuser.Email,otp)
        return {"message":"OTP sent succesfully!"}


def reset_password(user:ResetPass,otp:int,db:Session):

    dbuser=db.query(User).filter(User.OTP==otp).first()
    if dbuser.OTP!=otp:
        return {"message":"Invalid OTP"}
    if datetime.now()>dbuser.OTP_Expiry:
        return {"message":"OTP Expired"}
    
    dbuser.Password=pwd_context.hash(user.new_password)
    db.commit()
    return {"Message":"Password reset successful"}

def change_password(user:ChangePass,db:Session):

    dbuser=db.query(User).filter(User.Email==user.email).first()
    if not dbuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not Found!")
    
    if not verify_password(user.Current_Password,dbuser.Password):
        return {"Current password is incorrect"}
    if user.New_Password != user.Confirm_Password:
        return {"Passwords dont match"}
    
    dbuser.Password=pwd_context.hash(user.New_Password)
    db.commit()
    return {"Password changed succesfully"}
    
            
