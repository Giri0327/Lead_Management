from passlib.context import CryptContext
from dotenv import load_dotenv

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password: str):
    return pwd_context.verify(plain_password, password)


import smtplib
from email.mime.text import MIMEText
import os
load_dotenv()


def emailOTP(to:str,otp:int):

    myemail="keerthikk0302@gmail.com"
    mypass="gmxqefyobsuwwnnl"
    subject="Password reset link and OTP "
    body=f""" YOur OTP to reset pass is: {otp}

              This linnk expires in 15 minutes"""

    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=myemail
    msg["To"]=to

    print("Sending email to:",to)

    server= smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(myemail,mypass)
    server.send_message(msg)
    server.quit()
