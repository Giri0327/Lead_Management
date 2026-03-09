from abc import ABC,abstractmethod
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
import random
from datetime import datetime,timedelta,timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import *
#from app.schema import *
from app.models import User,Token
from app.schema import Tokens,Update_User,ForgotPass,ResetPass,ChangePass
from app.db import *
from app.core import *

from fastapi.security import OAuth2PasswordRequestForm

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
            #Phone = self.user.phone,
            Password = get_password_hash(self.user.password),
            #Role_ID=self.user.role_id,
            #Is_Active = self.user.is_active
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

    def view_users(self):
        users = self.db.query(User).all()
        return users

#USER LOGIN and OTP Generation
class Userabs(ABC):
    @abstractmethod
    def verify_user(self):
        pass


class Verify_user(Userabs):
        def __init__(self,db:Session,user_data):
             self.db=db
             self.user_data=user_data

        def verify_user(self):
             try:
                user = self.db.query(User).filter(
                        or_(
                        User.Username == self.user_data.username,
                        User.Email == self.user_data.username
                        )
                    ).first()
                if not user:
                    raise HTTPException(status_code=404,
                                        detail="User not found")
                
                verify_user_password = verify_password(self.user_data.password,user.Password)

                if not verify_user_password:
                    raise HTTPException(status_code=401,
                                        detail="Invalid Password")
                if not user.Is_two_fath:
                    token_gen = create_token(user)
                    self.db.query(Token).filter(Token.User_Id == user.User_ID).delete()
                    new_token = Token(User_Id = user.User_ID,
                                    Token = token_gen)
                    self.db.add(new_token)
                    self.db.commit()
                    print("Login")
                    return {"message":"Login successful",
                        "token": token_gen} 
                else:
                    otp = get_otp()
                    text = "OTP for your login "
                    expiry = datetime.utcnow()+ timedelta(minutes=10)
                    resetkey = reset_key()

                    user.OTP = otp
                    user.OTP_Expiry = expiry
                    user.Reset_Key = resetkey

                    self.db.commit()

                    emailOTP(user.Email, otp, text)
                    return {"message":"OTP sent to your email for verification","resetkey":resetkey}
                  
             except HTTPException:
                raise
             except Exception as e:
                print(e)   # show real error in terminal
                raise HTTPException(status_code=500, detail="Internal Server Error")
                        

#OTP and TOKEN VERIFICATION for USER          
class OTPToken(ABC):
    @abstractmethod
    def otp_verify(self):
        pass


class OTPTokenVerify(OTPToken):
    def __init__(self, db: Session, otp: int ,resetkey : str):
        self.db = db
        self.OTP = otp
        self.resetkey = resetkey

    def otp_verify(self):
        user = self.db.query(User).filter(User.Reset_Key == self.resetkey).first()

        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        # OTP check
        if self.OTP != user.OTP:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        else:
            if datetime.utcnow() > user.OTP_Expiry:
                raise HTTPException(status_code=400, detail="OTP expired")
            user.OTP = None
            user.OTP_Expiry = None
            user.Reset_Key = None
            self.db.commit()
            
            token_gen = create_token(user)
            self.db.query(Token).filter(Token.User_Id == user.User_ID).delete()
            new_token = Token(User_Id = user.User_ID,
                            Token = token_gen)
            self.db.add(new_token)
            self.db.commit()

            return {"message": "OTP Verified Successfully"}   

    
#FORGET PASSWORD
def forgot_password(user,db:Session):

    dbuser = db.query(User).filter(User.Email == user.email).first()

    if not dbuser:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "User not Found!")
    else:
        otp = get_otp()
        #print("OTP generated")
        expiry = (datetime.now(timezone.utc)+timedelta(minutes=10))
    
        text = "OTP for forget password"

        resetkey = reset_key()

        # dbuser.add(resetkey)   
        dbuser.Reset_Key = resetkey
        dbuser.OTP = otp
        dbuser.OTP_Expiry = expiry
        db.commit()

        emailOTP(dbuser.Email,otp,text)
        return {"message":"OTP sent succesfully!",
                "resetkey":resetkey}

#USER RESET PASSWORD
def reset_password(user,otp:int,reset_key:str,db:Session):
    dbuser = db.query(User).filter (User.Reset_Key == reset_key).first()

    if not dbuser:
        raise HTTPException(status_code=400, detail="Invalid reset key")

    if datetime.utcnow() > dbuser.OTP_Expiry:
        raise HTTPException(status_code=400, detail="OTP expired")

    if dbuser.OTP != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    dbuser.Password = pwd_context.hash(user.new_password)

    dbuser.OTP = None
    dbuser.OTP_Expiry = None
    dbuser.Reset_Key = None
    db.commit()

    return {
        "Message": "Password reset successful"
    }

#USER CHANGE PASSWORD
def change_password(user,db:Session):

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
    
            

                           