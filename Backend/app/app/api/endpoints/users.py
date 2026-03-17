from fastapi import APIRouter, Depends,BackgroundTasks,Request
from sqlalchemy.orm import Session
from app.db import session,get_db
from sqlalchemy.orm import Session
from app.crud import ADDUser,forgot_password,reset_password,OTPTokenVerify,Verify_user,Resend_OTP,UpdateUser
from app.schema import UserInfo,ForgotPass,ResetPass,ChangePass,UserVerify,UserLogin,resend_otp
from app.core import oauth2_scheme    
from app.api.deps import role_required 
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import Form

#router
router =APIRouter(prefix="/user",tags=["User"])

#CREATING USER

@router.post("/Signup")
async def CreateUser(user:UserInfo,db:Session = Depends(get_db)):
    x= ADDUser(user,db)
    return x.Create_user()

@router.get("/Adminview_Users")
async def ViewUser(current_user = Depends(role_required([1])),db:Session=Depends(get_db)):
    x=ADDUser(None,db)
    return x.view_users()


@router.put("/AdminUpdatesUsers")
async def Admin_Upd_user(
    user_id: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    user_role : str =Form(...),
    phone: str = Form(...),

    current_user = Depends(role_required([1])),
    db: Session = Depends(get_db)
):
    x = UpdateUser(None, db)

    return x.AdminUser_Update(
        user_id,
        first_name,
        last_name,
        email,
        user_role,
        phone
    )



@router.put("/UpdateUser")
async def update_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    file: UploadFile = File(...),

    current_user = Depends(role_required([2])),
    db: Session = Depends(get_db)
):
    
    service = UpdateUser(None,db)

    return service.Update_user(
        current_user["user_id"],
        first_name,last_name,
        email,phone,file
    )

@router.put("/Twofath")
async def TwoFATH(current_user = Depends(role_required([2])),db:Session = Depends(get_db)):
    x=UpdateUser(current_user,db)
    return x.Twofath(current_user)

@router.put("/Logout")
async def Logout(current_user = Depends(role_required([1,2])),db:Session = Depends(get_db)):
    x=UpdateUser(current_user,db)
    return x.Logout(current_user)

@router.post("/change_password")
async def Change_Pass(user:ChangePass,current_user = Depends(role_required([2])),
                      db:Session = Depends(get_db)):
    x=UpdateUser(user,db)
    return x.change_password(current_user)

@router.post("View_UserBy_id")
async def view_by_id(current_user = Depends(role_required([1,2])),db:Session=Depends(get_db)):
    x=ADDUser(None,db)
    return x.view_userby_id(current_user)
    
#RESET PASSWORD USING FORGT PASSWORD

@router.post("/forgot_password")
async def forgot_pass(user: ForgotPass, background_tasks:BackgroundTasks,
                      #current_user = Depends(role_required([1,2])),
                      db: Session = Depends(get_db)):
    
    return forgot_password(user, db,background_tasks)

@router.post("/reset_password")
async def Reset_Pass(user:ResetPass,otp:int,reset_key:str,
                     #current_user = Depends(role_required([1,2])),
                     db:Session = Depends(get_db)):
    return reset_password(user,db)


#LOGIN FUNCTIONS

@router.post("/Login")
async def UserLogin(background_task:BackgroundTasks,request:Request,user_data:UserLogin,db:Session=Depends(get_db)):
    login= Verify_user(db,request,background_task,user_data)
    result = login.verify_user()
    return result  

@router.post("/Otpverify")
async def Otpverify(user: UserVerify, db: Session = Depends(get_db)):
    x = OTPTokenVerify(db,  user.otp, user.resetkey)
    result = x.otp_verify()
    return result 

@router.post("/resendOTP")
async def ResendOTP(user:resend_otp,background_task:BackgroundTasks,db:Session=Depends(get_db)):
    return Resend_OTP(user.reset_key,db,background_task)



'''from app.db import Base,engine

@router.post("/createDB")
async def db():
    return Base.metadata.create_all(bind=engine)'''

