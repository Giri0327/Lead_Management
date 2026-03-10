from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Stage(Base):

    __tablename__ = "stage"

    Stage_ID = Column(Integer,primary_key=True,autoincrement=True)
    stage = relationship("Lead",back_populates="lead_stage") 

    Stage_Name = Column(String(255))

    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())
