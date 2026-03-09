from fastapi import Depends
from passlib.context import CryptContext
import jwt 
from datetime import datetime as dt
from datetime import timedelta
import random 
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from app.models import User
import os
load_dotenv()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password: str):
    return pwd_context.verify(plain_password, password)

SECRET_KEY = "kscubauekasdbcusebfvisuboa58utsjkndc%"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 5

def create_token(user:User):
    payload={
        "user_id":user.User_ID,
        "username":user.Username,
        "role":user.Role_ID,
        "exp":dt.now()+timedelta(minutes=EXPIRE_MINUTES)
    }

    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        return "Token Expired"
    except jwt.InvalidTokenError:
        return "Invalid Token"

#Get User Information    
'''
payload = decode_token(token):
user_id = payload["user_id"]
user_name = payload["username"]
user_role = payload["role"]
'''    

def get_otp():
    otp = random.randint(100000,999999)
    return otp  



def emailOTP(to:str,otp:int,text:str):

    myemail = "keerthikk0302@gmail.com"
    mypass ="gmxqefyobsuwwnnl"
    subject = text
    body=f""" YOur OTP to reset pass is: {otp}

              This otp expires in 15 minutes"""

    msg=MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = myemail
    msg["To"] = to

    print("Sending email to:",to)

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(myemail,mypass)
    server.send_message(msg)
    server.quit()

