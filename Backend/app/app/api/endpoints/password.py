from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import password
from app.schema import *
router =APIRouter()


@router.post("/forgot_password")
async def forgot_pass(user: ForgotPass, db: Session = Depends(get_db)):
    print("Received:", user)
    return password.forgot_password(user, db)

@router.post("/reset_password")
async def Reset_Pass(user:ResetPass,otp:int,db:Session=Depends(get_db)):
    return password.reset_password(user,otp,db)

@router.post("/change_password")
async def Change_Pass(user:ChangePass,db:Session=Depends(get_db)):
    return password.change_password(user,db)