from sqlalchemy import Column,String,Integer,Text,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Follow_Up(Base):

    __tablename__ = "follow_up"

    Follow_Up_ID = Column(Integer,primary_key=True,autoincrement=True)

    User_ID  = Column(Integer,ForeignKey("user.User_ID",ondelete = "CASCADE")) #FK
    user = relationship("User",back_populates = "follow_ups")

    Lead_ID = Column(Integer,ForeignKey("lead_data.Lead_ID"))
    lead_id = relationship("Lead",back_populates = "lead")

    Contact_Type = Column(String(255),nullable = False)
    Notes = Column(Text)
    Contacted_On = Column(DateTime)
    Status = Column(Boolean)

    Created_At= Column(DateTime,server_default = func.now())



