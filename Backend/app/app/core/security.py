from passlib.context import CryptContext
import jwt 
from datetime import datetime as dt
from datetime import timedelta
import random 
import smtplib
from email.message import EmailMessage

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    expire = dt.now()+timedelta(minutes=EXPIRE_MINUTES)
    user_token.update({"exp":expire})
    return jwt.encode(user_token,SECRET_KEY,algorithm=ALGORITHM)

def get_otp(email):
    otp = ""

    for i in range(6):
        otp+=str(random.randint(0,9))

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('girinath0327@gmail.com','wizi mybw gliz ilav')
    to_mail = email

    msg = EmailMessage()

    msg['Subject'] = "OTP Verification"
    msg['From'] = 'girinath0327@gmail.com'
    msg['To'] = to_mail
    msg.set_content('You have one-time password to reset your password \n  Your_otp_is: '+ otp)
    server.send_message(msg)
    server.quit()
    print("Otp sent successfully")
    return otp    