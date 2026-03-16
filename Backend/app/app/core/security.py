import datetime
from fastapi import Request as request
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
#from app.api.endpoints.users import Logout
from app.models import User
import os
from zoneinfo import ZoneInfo
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi.security import OAuth2PasswordBearer



load_dotenv()


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/user/Login")

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password: str):
    return pwd_context.verify(plain_password, password)

SECRET_KEY = "kscubauekvisubojnafwuerua58utsjkndc"
ALGORITHM = "HS256"

def create_token(user):
    
    now = dt.now()
    expire = now.replace(hour=23, minute=59, second=59, microsecond=0)
    #if login time is alomst to expire time reset to sext day
    if expire <= now:
        expire = expire.replace(day=expire.day + 1)
    payload={
        "user_id":user.User_ID,
        "username":user.Username,
        "role":user.Role_ID,
        "exp":expire
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token


def get_device_type(user_agent:str):
    if "Mobile" in user_agent:
        return "Mobile"
    elif "Tablet" in user_agent:
        return "Tablet"
    else:
        return "Desktop"


def decode_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id = payload["user_id"]
        role_id = payload["role"]
        return {"user_id":user_id,
                "role":role_id}
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
    body=f""" Your OTP to reset pass is: {otp}

              This otp expires in 2 minutes"""

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

def reset_key():
    s = os.getenv("resetkey")
    reset_key = ""

    for i in range(30):
        reset_key += random.choice(s)

    print("Generated reset_key:", reset_key)
    return reset_key


# Configuration       
cloudinary.config( 
    cloud_name = os.getenv("cloud_name"),
    api_key = os.getenv("api_key"), 
    api_secret = os.getenv("api_secret"), # Click 'View API Keys' above to copy your API secret
    secure=True
)

# cloud_name=dedavidqu
# api_key=444542291171161

# api_secret=hjpewQPZilRXNVpZf9GHmIJj_cI