from fastapi import APIRouter, Depends,BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.db import session,get_db
from sqlalchemy.orm import Session
from app.crud import ADDUser,forgot_password,reset_password,change_password,verify_password,OTPTokenVerify,Verify_user
from app.schema import UserInfo,Update_User,ForgotPass,ResetPass,ChangePass,UserVerify,UserLogin
from app.core import oauth2_scheme


#router
router =APIRouter(prefix="/user",tags=["User"])


@router.post("/CreateUser")
async def CreateUser(user:UserInfo,db:session = Depends(get_db)):
    x= ADDUser(user,db)
    return x.Create_user()

@router.put("/UpdateUser/{user_id}")
async def update_user(user_id: int, user: Update_User, db: session = Depends(get_db)):
    user_service = ADDUser(user, db)
    return user_service.Update_user(user_id)

@router.get("/view_Users")
async def ViewUser(token:str=Depends(oauth2_scheme),db:session=Depends(get_db)):
    x=ADDUser(None,db)
    return x.view_users()

# view_users(db: session = Depends(get_db)):

@router.post("/forgot_password")
async def forgot_pass(user: ForgotPass, background_tasks:BackgroundTasks,db: session = Depends(get_db)):
    return forgot_password(user, db,background_tasks)

@router.post("/reset_password")
async def Reset_Pass(user:ResetPass,otp:int,reset_key:str,db:session = Depends(get_db)):
    return reset_password(user,otp,reset_key,db)

@router.post("/change_password")
async def Change_Pass(user:ChangePass,token:str,db:session = Depends(get_db)):
    return change_password(user,token,db)

# oauth2_scheme = OAuth2PasswordRequestForm(token_url)
@router.post("/Login")
async def UserLogin(background_tasks:BackgroundTasks,user:UserLogin,db:Session=Depends(get_db)):
    login= Verify_user(db,user,background_tasks)
    result = login.verify_user()
    return result  

@router.post("/Otpverify")
async def Otpverify(user: UserVerify, db: session = Depends(get_db)):
    x = OTPTokenVerify(db,  user.otp, user.resetkey)
    result = x.otp_verify()
    return result 

"""@router.post("/createDB")
async def db():
    return Base.metadata.create_all(bind=engine)"""