from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Database
from app.db.session import get_db, engine
from app.db.base_class import Base

# CRUD operations
from app.crud import *

# Schemas
from app.schema import *



#router
router =APIRouter(prefix="/user",tags=["User"])


@router.post("/CreateUser")
async def CreateUser(user:UserInfo,db:Session = Depends(get_db)):
    x= ADDUser(user,db)
    return x.Create_user()

@router.put("/UpdateUser/{user_id}")
async def update_user(user_id: int, user: Update_User, db: Session = Depends(get_db)):
    user_service = ADDUser(user, db)
    return user_service.Update_user(user_id)

@router.get("/view_Users")
async def ViewUser(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    x=ADDUser(None,db)
    return x.view_users()

# view_users(db: Session = Depends(get_db)):

@router.post("/forgot_password")
async def forgot_pass(user: ForgotPass, db: Session = Depends(get_db)):
    print("Received:", user)
    return forgot_password(user, db)

@router.post("/reset_password")
async def Reset_Pass(user:ResetPass,otp:int,reset_key:str,db:Session = Depends(get_db)):
    return reset_password(user,otp,reset_key,db)

@router.post("/change_password")
async def Change_Pass(user:ChangePass,db:Session = Depends(get_db)):
    return change_password(user,db)

# oauth2_scheme = OAuth2PasswordRequestForm(token_url)
@router.post("/Login")
async def UserLogin(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    login= Verify_user(db,form_data)
    result = login.verify_user()
    return result  

@router.post("/Otpverify")
async def Otpverify(user: OTPVerify, db: Session = Depends(get_db)):
    x = OTPTokenVerify(db, user.email, user.otp, user.otp)
    result = x.otp_verify()
    return result

"""@router.post("/createDB")
async def db():
    return Base.metadata.create_all(bind=engine)"""