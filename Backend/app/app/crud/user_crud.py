from app.db import session
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import or_
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

class Userabs(ABC):
    @abstractmethod
    def create_user():
        pass

class Verify_user(Userabs):
        def __init__(self,db:Session,user_data):
             self.db=db
             self.user_data=user_data

        def verify_user(self):
             user=self.db.query(User).filter(
                or_(
                User.user_name == self.user_data.identifier,User.email == self.user_data.identifier)
                ).first()  
             if not user:
                  return "Invalid Credientials"
                           