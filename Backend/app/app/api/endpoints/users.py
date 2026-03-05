from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.User_crud import Create_user
from app.schema.User_Schema import User
router =APIRouter(prefix="/user",tags=["User"])


@router.post("/CreateUser")
async def CreateUser(user:User,db:Session=Depends(get_db)):
    return Create_user(user,db)

