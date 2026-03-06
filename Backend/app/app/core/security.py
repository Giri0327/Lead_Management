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
import os
load_dotenv()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password: str):
    return pwd_context.verify(plain_password, password)

SECRET_KEY = "$argon2id$v=19$m=65536,t=3,p=4$MqbU2rs3hlCKUWrt3ZvTeg$x7NxVTgTBPlJkRL/+WLpgoDttc+8IG6I0NTzDwwzJsk"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 5

def create_token(data):
    user_token = {}
    user_token.update(data)
    expire = dt.now()+timedelta(minutes = EXPIRE_MINUTES)
    user_token.update({"exp":expire})
    return jwt.encode(user_token,SECRET_KEY,algorithm = ALGORITHM)


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
