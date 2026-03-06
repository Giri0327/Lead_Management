from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Database
from app.db.session import get_db, engine
from app.db.base_class import Base
# CRUD operations
from app.crud.user_crud import (Create_user,forgot_password,reset_password,change_password,Verify_user,OTPTokenVerify)
# Schemas
from app.schema.User_Schema import (User,OTPVerify,ForgotPass,ResetPass,ChangePass,UserLogin)


#router
router =APIRouter(prefix="/user",tags=["User"])


@router.post("/CreateUser")
async def CreateUser(user:User,db:Session=Depends(get_db)):
    return Create_user(user,db)

@router.post("/forgot_password")
async def forgot_pass(user: ForgotPass, db: Session = Depends(get_db)):
    print("Received:", user)
    return forgot_password(user, db)

@router.post("/reset_password")
async def Reset_Pass(user:ResetPass,otp:int,db:Session=Depends(get_db)):
    return reset_password(user,otp,db)

@router.post("/change_password")
async def Change_Pass(user:ChangePass,db:Session=Depends(get_db)):
    return change_password(user,db)

 
@router.post("/Login")
async def UserLogin(user:UserLogin,db:Session=Depends(get_db)):
    login= Verify_user(db,user)
    result = login.verify_user()
    return result  

@router.post("/Otpverify")
async def Otpverify(user: OTPVerify, db: Session = Depends(get_db)):
    x = OTPTokenVerify(db, user.email, user.otp)
    result = x.otp_verify()
    return result

"""@router.post("/createDB")
async def db():
    return Base.metadata.create_all(bind=engine)"""