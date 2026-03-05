from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.User_Table import User
from app.models.Tokens_Table import Token
from abc import ABC,abstractmethod
from app.schema import *
from sqlalchemy.orm import Session
from app.models import *
from app.db import *
import random
from datetime import datetime,timedelta
from app.core import pwd_context,verify_password
from app.core.security import get_otp,create_token
from fastapi import HTTPException,status
#CREATE USER
def Create_user(user,db:Session):
    x=User(Username=user.username,
           First_Name=user.first_name,
           Last_Name=user.last_name,
           Email=user.email,
           Phone=user.phone,
           Password=get_password_hash(user.password),
           Role_ID=user.role_id,
           Is_Active=user.is_active
           )
    db.add(x)
    db.commit()
    db.refresh(x)
    if x is not None:   
        return "User created successfully"  

#USER LOGIN    

class Userabs(ABC):
    @abstractmethod
    def verify_user():
        pass

class Verify_user(Userabs):
        def __init__(self,db:Session,user_data):
             self.db=db
             self.user_data=user_data

        def verify_user(self):
             user = self.db.query(User).filter(
                or_(
                User.Username == self.user_data.username_or_email,User.Email == self.user_data.username_or_email)
                ).first()  
             if not user:
                  return "Invalid Credientials"
             verify_user_password = verify_password(self.user_data.password,user.Password)
             send_otp = get_otp(email=user.Email)
             self.db.query(User).filter(User.Email == user.Email).update({User.OTP: send_otp})
             self.db.commit()

             token_gen = create_token(data = {"sub": user.User_ID})
             self.db.query(Token).filter(Token.User_Id == user.User_ID).delete()
             new_token =Token(User_Id=user.User_ID,
                              token=token_gen)
             self.db.add(new_token)
             self.db.commit()

             if not verify_user_password:
                  return "Invalid Password"
             



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

        get_otp(email=user.Email)
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
    
            

                           