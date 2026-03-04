from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "user"


    User_ID = Column(Integer,primary_key=True)
    leads_user_note = relationship("Lead_Notes",back_populates="leads_note")
    lead_activity  =relationship("Lead_Activity",back_populates="lead_user")
    follow_ups = relationship("Follow_Up",back_populates="user")


    Username = Column(String(255),unique=True,nullable=False)
    First_Name = Column(String(255),nullable=False)
    Last_Name = Column(String(255),nullable=True)
    Email = Column(String(255),nullable=False)
    Phone = Column(String(12),nullable=False)
    Profile_Pic_URL = Column(String(255))
    Password= Column(String(255),nullable=False)
    OTP= Column(Integer)
    OTP_Expiry= Column(DateTime)

    Role_ID = Column(Integer,ForeignKey("roles.Role_ID"))  #FK
    role_id_user = relationship("Roles",back_populates="roles")

    Is_Active = Column(Boolean,default=False)
    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())

    user_token = relationship("Token",back_populates="token")

    owner = relationship("Lead",back_populates="leads")



