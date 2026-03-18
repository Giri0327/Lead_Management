from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from fastapi import Request as request
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_
from app.models import *
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.orm import Session
from app.models import User, Token
from app.schema import ForgotPass, ResetPass, UserVerify
from app.core import (
    get_password_hash,
    verify_password,
    create_token,
    get_otp,
    emailOTP,
    reset_key,
    pwd_context,
)
from app.core.security import cloudinary, get_device_type


# CREATE USER
class ADDUser:
    def __init__(self, user, db: Session):
        self.user = user
        self.db = db

    def Create_user(self):
        # throws error if username already exist
        exist_username = (
            self.db.query(User).filter(User.Username == self.user.username).first()
        )
        if exist_username:
            raise HTTPException(status_code=404, detail="Username Aleady Exist")
        # throws error if email already exist
        exist_email = self.db.query(User).filter(User.Email == self.user.email).first()
        if exist_email:
            raise HTTPException(status_code=404, detail="Email already Exist")
        x = User(
            Username=self.user.username,
            First_Name=self.user.first_name,
            Last_Name=self.user.last_name,
            Email=self.user.email,
            Phone=self.user.phone,
            Password=get_password_hash(self.user.password),
            Role_ID=self.user.role_id,
            Is_Active=self.user.is_active,
        )

        self.db.add(x)
        self.db.commit()
        self.db.refresh(x)
        if x is not None:
            return "User created successfully"

    # Admin can view user with their user_id
    def view_userby_id(self, current_user):

        user_id = current_user["user_id"]
        user = (
            self.db.query(
                User.First_Name,
                User.Last_Name,
                User.Email,
                Roles.Role_Name,
                User.Phone,
                User.Profile_Pic_URL,
            )
            .join(Roles, User.Role_ID == Roles.Role_ID)
            .filter(User.User_ID == user_id)
            .first()
        )
        if user:
            return user._asdict()

        return None

    # view all users by the admin
    def view_users(self):

        users = (
            self.db.query(
                User.User_ID,
                User.First_Name,
                User.Last_Name,
                User.Email,
                User_Role.user_role,
                User.Phone,
            )
            .join(User_Role, User.User_Role_id == User_Role.User_Role_id)
            .all()
        )

        return [row._asdict() for row in users]


class UpdateUser:
    def __init__(self, user, db: Session):
        self.user = user
        self.db = db

    # user can update their user profile
    def Update_user(self, current_user, first_name, last_name, email, phone):
        usr = current_user["user_id"]

        query = self.db.query(User).filter(User.User_ID == usr).first()
        if not query:
            raise HTTPException(status_code=404, detail="Invalid User")

        email_exist = (
            self.db.query(User)
            .filter(User.User_ID != usr, or_(User.Email == email, User.Phone == phone))
            .first()
        )

        if email_exist:
            if email_exist.Email == email:
                raise HTTPException(status_code=400, detail="Email already exists")
            if email_exist.Phone == phone:
                raise HTTPException(status_code=400, detail="Phone already exists")

        query.Email = email
        query.First_Name = first_name
        query.Last_Name = last_name
        query.Phone = phone
        self.db.commit()

        return {
            "message": "User updated successfully",
        }

    def Update_user_pic(self, current_user, file):
        try:
            user = current_user["user_id"]
            query = self.db.query(User).filter(User.User_ID == user).first()

            filename = file.filename.lower()

            if not filename.endswith((".png", ".jpg", ".jpeg")):
                raise HTTPException(
                    status_code=400, detail="Only PNG and JPEG images are allowed"
                )
            filename = file.filename.split(".")[0]
            extension = file.filename.split(".")[1]

            result = cloudinary.uploader.upload(file.file,
            public_id=filename,
            format=extension)
            # image_url = result["secure_url"]
            version = result["version"]
            public_id = result["public_id"]

            url = f"https://res.cloudinary.com/dedavidqu/image/upload/v{version}/{public_id}.{extension}"

    
            short_url = url.replace(
                "https://res.cloudinary.com/dedavidqu/image/upload/",
                "CLOUDINARY/"
            )

            print(short_url)
            
            query.Profile_Pic_URL = short_url

            self.db.commit()
            self.db.refresh(query)


            return "Upload successfull"
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, details="Bad Request"
            )

    # Admin can update the users Profile with his admin Access
    def AdminUser_Update(self, user_id, first_name, last_name, email, user_role, phone):

        user = self.db.query(User).filter(User.User_ID == user_id).first()

        if not user:
            return {"message": "User not found"}

        user.First_Name = first_name
        user.Last_Name = last_name
        user.Email = email
        user.Phone = phone
        user.User_Role_id = user_role  # if role_id is stored

        self.db.commit()
        self.db.refresh(user)

        return {"message": "User updated successfully"}

    # Logout Fucntion Deletes token and updates Logout time in DB
    def Logout(self, current_user):
        user_id = current_user["user_id"]
        user = (
            self.db.query(Token)
            .filter(Token.User_Id == user_id)
            .order_by(Token.Created_At.desc())
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="Invalid User")

        user.Token = None
        user.update_At = datetime.utcnow()  # optional if DB auto-updates

        self.db.commit()
        self.db.refresh(user)

        return {"message": "Logout Success"}

    # User can Enabel or Disable the TwoFactor Authencation for Security
    def Twofath(self, current_user):
        user_id = current_user["user_id"]
        user = self.db.query(User).filter(User.User_ID == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Invalid User")

        user.Is_two_fath = not user.Is_two_fath
        self.db.commit()

        if user.Is_two_fath:
            return "Two Factor authentication Enabled"
        else:
            return "Two Factor authentication Disabled"

    # User Can change their Password In the profile Security without authentication when they know their old password
    def change_password(self, current_user):
        user_id = current_user["user_id"]

        new = self.db.query(User).filter(User.User_ID == user_id).first()
        if not new:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not verify_password(self.user.Current_Password, new.Password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )
        if not self.user.New_Password == self.user.Confirm_Password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                details="Password doesn't match",
            )
        new.Password = pwd_context.hash(self.user.New_Password)

        self.db.commit()

        return {"message": "Password changed Succesfully"}


# USER LOGIN and OTP Generation
class Userabs(ABC):
    @abstractmethod
    def verify_user(self):
        pass


class Verify_user(Userabs):
    def __init__(self, db: Session, request, background_task, user_data):
        self.db = db
        self.user_data = user_data
        self.request = request
        self.background_task = background_task

    # Verify user and password for login
    def verify_user(self):
        try:
            user = (
                self.db.query(User)
                .filter(
                    or_(
                        User.Username == self.user_data.username_or_email,
                        User.Email == self.user_data.username_or_email,
                    )
                )
                .first()
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Credentials",
                )

            verify_user_password = verify_password(
                self.user_data.password, user.Password
            )

            if not verify_user_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Credentials",
                )
            if not user.Is_two_fath:
                token_gen = create_token(user)
                user_agent = self.request.headers.get("user-agent", "")
                device_type = get_device_type(user_agent)
                token_expiry = datetime.utcnow()

                """self.db.query(Token).filter(Token.User_Id == user.User_ID).delete()"""
                # creates token when user is without twofath auth
                new_token = Token(
                    User_Id=user.User_ID,
                    Device_Type=device_type,
                    Token_Expiry=token_expiry,
                    Token=token_gen,
                )
                self.db.add(new_token)
                # self.db.add()
                self.db.commit()
                self.db.refresh(new_token)
                return {"message": "Login successful", "token": token_gen}

            # generates otp is user has Twofath authentication
            else:
                otp = get_otp()
                text = "OTP for your login "
                expiry = datetime.utcnow() + timedelta(minutes=5)
                resetkey = reset_key()

                user.OTP = otp
                user.OTP_Expiry = expiry
                user.Reset_Key = resetkey

                self.db.commit()

                self.background_task.add_task(emailOTP, user.Email, otp, text)
                return {
                    "message": "OTP sent to your email for verification",
                    "resetkey": resetkey,
                }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")


# OTP and TOKEN VERIFICATION for USER


class OTPToken(ABC):
    @abstractmethod
    def otp_verify(self):
        pass


class OTPTokenVerify(OTPToken):
    def __init__(self, db: Session, request, otp: int, resetkey: str):
        self.db = db
        self.OTP = otp
        self.resetkey = resetkey
        self.request = request

    # verify otp with the generated reset key
    def otp_verify(self):

        user = self.db.query(User).filter(User.Reset_Key == self.resetkey).first()

        if not user:
            raise HTTPException(status_code=404, detail="Not found")

        # OTP check
        if self.OTP != user.OTP:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        else:
            if datetime.utcnow() > user.OTP_Expiry:
                user.OTP = None
                user.OTP_Expiry = None
                raise HTTPException(status_code=400, detail="OTP expired")

            user.OTP = None
            user.OTP_Expiry = None
            user.Reset_Key = None
            self.db.commit()

            token_gen = create_token(user)
            user_agent = self.request.headers.get("user-agent", "")
            device_type = get_device_type(user_agent)
            new_token = Token(
                User_Id=user.User_ID, Device_Type=device_type, Token=token_gen
            )
            self.db.add(new_token)
            self.db.commit()
            self.db.refresh(new_token)

            return {
                "message": "OTP Verified Successfully",
                "messgae2": "Login Success",
                "token": token_gen,
            }


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    # RESEND OTP
    def resend_otp(self, reset_key, background_tasks):

        user = self.db.query(User).filter(User.Reset_Key == reset_key).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if datetime.utcnow() < user.OTP_Expiry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP still valid. Please wait before requesting a new OTP",
            )

        new_otp = get_otp()
        expiry = datetime.utcnow() + timedelta(seconds=45)

        user.OTP = new_otp
        user.OTP_Expiry = expiry

        self.db.commit()

        text = "You have entered a resend otp - OTP for your login is "
        background_tasks.add_task(emailOTP, user.Email, new_otp, text)

        return {"message": "OTP Resent Successfully"}

    # FORGOT PASSWORD
    def forgot_password(self, user: ForgotPass, background_tasks):

        dbuser = self.db.query(User).filter(User.Email == user.email).first()

        if not dbuser:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not Found!"
            )

        otp = get_otp()
        expiry = datetime.utcnow() + timedelta(minutes=10)

        resetkey = reset_key()

        dbuser.Reset_Key = resetkey
        dbuser.OTP = otp
        dbuser.OTP_Expiry = expiry

        self.db.commit()

        text = "OTP for forget password"
        background_tasks.add_task(emailOTP, dbuser.Email, otp, text)

        return {"message": "OTP sent successfully!", "resetkey": resetkey}

    # VERIFY OTP
    def reset_otp_verify(self, user: UserVerify):

        dbuser = self.db.query(User).filter(User.Reset_Key == user.resetkey).first()

        if not dbuser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset key"
            )

        if datetime.utcnow() > dbuser.OTP_Expiry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired"
            )

        if dbuser.OTP != user.otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        return {"Message": True, "resetkey": dbuser.Reset_Key}

    # RESET PASSWORD
    def reset_password(self, user: ResetPass):

        dbuser = self.db.query(User).filter(User.Reset_Key == user.resetkey).first()

        if not dbuser:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reset key mismatched"
            )

        dbuser.Password = pwd_context.hash(user.new_password)

        dbuser.Reset_Key = None
        dbuser.OTP = None
        dbuser.OTP_Expiry = None

        self.db.commit()

        return {"message": "Password Reset Successful"}
