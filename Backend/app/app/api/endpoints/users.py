from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.User_crud import Create_user,forgot_password,reset_password,change_password
from app.schema.User_Schema import User
from app.schema import *
from app.db.base_class import Base
from app.db.session import engine
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

#@router.post("/createDB")
async def db():
    Base.metadata.create_all(bind=engine) 