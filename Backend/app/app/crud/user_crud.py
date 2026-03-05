from app.db import session
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.models.User_Table import User
from abc import ABC,abstractmethod
#CREATE USER
def Create_user(user,db:Session):
    x=User(Username=user.username,
           First_Name=user.first_name,
           Last_Name=user.last_name,
           Email=user.email,
           Phone=user.phone,
           Profile_Pic_URL=user.profile_pic,
           Password=get_password_hash(user.password),
           Role_ID=user.role_id,
           Is_Active=user.is_active
           )
    db.add(x)
    db.commit()
    db.refresh(x)
    if x is not None:   
        return "User created successfully"  

#USER LOGIN    

'''class Userabs(ABC):
    @abstractmethod
    def create_user():
        pass

class Verify_user(Userabs):
        def __init__(self,db:Session,):'''
             