from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class User_Role(Base):

    __tablename__ = "user_role"

    User_Role_id = Column(Integer,primary_key =True)

    user_role = Column(String(255))

    Created_At= Column(DateTime,server_default=func.now())
   
    user = relationship("User",back_populates="user_role")
    # Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())


