from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Token(Base):

    __tablename__ = "token"

    Token_ID = Column(Integer,primary_key=True,autoincrement=True)

    User_Id = Column (Integer,ForeignKey("user.User_ID"))  #FK
    user = relationship("User",back_populates="user_token")

    Token = Column(String(255))
    Token_Expiry = Column(DateTime)
    Device_Type = Column(String(100))
    Created_At= Column(DateTime,server_default=func.now())





