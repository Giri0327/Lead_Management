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
from datetime import datetime,timedelta,timezone
from app.core import pwd_context,verify_password
from app.core.security import create_token,emailOTP,get_otp
from fastapi import HTTPException,status

#CREATE USER
class ADDUser:
    def __init__(self,user,db:Session):
        self.user = user
        self.db = db
        
    def Create_user(self):
        x=User(Username = self.user.username,
            First_Name = self.user.first_name,
            Last_Name = self.user.last_name,
            Email = self.user.email,
            Phone = self.user.phone,
            Password = get_password_hash(self.user.password),
            #Role_ID=self.user.role_id,
            Is_Active = self.user.is_active
            )
        self.db.add(x)
        self.db.commit()
        self.db.refresh(x)
        if x is not None:   
            return "User created successfully"  
        
    def Update_user(self,user_id):
        user = self.db.query(User).filter(User.User_ID == user_id).first()
        if not user:
            raise HTTPException(status_code=404,
                                detail="Invalid User")
        user.Username = self.user.username
        user.First_Name = self.user.first_name
        user.Last_Name = self.user.last_name
        user.Email = self.user.email
        user.Phone = self.user.phone
        user.Profile_Pic_URL = self.user.profile_pic_URL
        user.Is_two_fath = self.user.Is_two_fath

        self.db.commit()
        self.db.refresh(user)

        return "User updated successfully"

def view_users(db:Session):
    users = db.query(User).all()
    return users

#USER LOGIN and OTP Generation
class Userabs(ABC):
    @abstractmethod
    def verify_user():
        pass

class Verify_user(Userabs):
        def __init__(self,db:Session,user_data):
             self.db=db
             self.user_data=user_data

        def verify_user(self):
             try:
                user = self.db.query(User).filter(
                    or_(
                    User.Username == self.user_data.username_or_email,User.Email == self.user_data.username_or_email)
                    ).first()  
                if not user:
                    raise HTTPException(status_code=404,
                                        detail="User not found")
                
                verify_user_password = verify_password(self.user_data.password,user.Password)

                if not verify_user_password:
                    raise HTTPException(status_code=404,
                                        detail="Invalid Password")
                
                token_gen = create_token(data = {"sub": user.User_ID})
                self.db.query(Token).filter(Token.User_Id == user.User_ID).delete()
                new_token = Token(User_Id = user.User_ID,
                                Token = token_gen)
                self.db.add(new_token)
                self.db.commit()
                print("Login")
                if user.Is_two_fath:
                    otp =get_otp()
                    print("OTP generated")
                    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)


                    text = "OTP for your Login verification"
                    user.OTP = otp
                    user.OTP_Expiry = expiry
                    self.db.commit()
                    self.db.refresh(user)
                    emailOTP(user.Email,otp,text)

             except Exception as e:
                 return {"Error:", e}

#OTP and TOKEN VERIFICATION for USER          
class OTPToken(ABC):
    @abstractmethod
    def otp_verify(self):
        pass


class OTPTokenVerify(OTPToken):
    def __init__(self, db: Session, email: str, otp: int ,token : str):
        self.db = db
        self.Email = email
        self.OTP = otp
        self.token = token

    def otp_verify(self):
        user = self.db.query(User).filter(User.Email == self.Email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # OTP check
        if user.OTP != self.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # give error if otp expired
        if datetime.now(timezone.utc) > user.OTP_Expiry:
            raise HTTPException(status_code=400, detail="OTP expired")

        #verify token
        token_check = self.db.query(Token).filter(
            Token.User_Id == user.User_ID,
            Token.Token == self.token
            ).first()

        if not token_check:
            raise HTTPException(status_code=400, detail="Invalid Token")
        
        #use If token expiry added
        '''if datetime.now(timezone.utc) > token_check.Token_Expiry:
            raise HTTPException(status_code=400, detail="Token expired")'''
        
        # otp clear
        user.OTP = None
        user.OTP_Expiry = None

        self.db.commit()

        return {"message": "OTP Verified Successfully"}     
    
#FORGET PASSWORD
def forgot_password(user:ForgotPass,db:Session):

    dbuser = db.query(User).filter(User.Email == user.email).first()

    if not dbuser:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "User not Found!")
    else:
        otp = get_otp()
        print("OTP generated")
        expiry = (datetime.now()+timedelta(minutes=10))
    
        text = "OTP for forget password"
        dbuser.OTP = otp
        dbuser.OTP_Expiry = expiry
        db.commit()

        emailOTP(dbuser.Email,otp,text)
        return {"message":"OTP sent succesfully!"}

#USER RESET PASSWORD
def reset_password(user:ResetPass,otp:int,db:Session):

    dbuser=db.query(User).filter(User.OTP == otp).first()
    if not dbuser:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if datetime.now()>dbuser.OTP_Expiry:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    dbuser.Password = pwd_context.hash(user.new_password)
    db.commit()
    return {"Message":"Password reset successful"}

#USER CHANGE PASSWORD
def change_password(user:ChangePass,db:Session):

    dbuser = db.query(User).filter(User.Email == user.email).first()
    if not dbuser:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "User not Found!")
    
    if not verify_password(user.Current_Password,dbuser.Password):
        return {"Current password is incorrect"}
    if user.New_Password != user.Confirm_Password:
        return {"Passwords dont match"}
    
    dbuser.Password = pwd_context.hash(user.New_Password)
    db.commit()
    return {"Password changed succesfully"}
    
            

                           