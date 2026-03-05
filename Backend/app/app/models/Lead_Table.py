from sqlalchemy import Column,Text,String,Integer,DECIMAL,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Lead(Base):

    __tablename__ = "lead"

    Lead_ID = Column(Integer,primary_key=True) ##

    lead= relationship("Follow_Up",back_populates="lead_id")
    lead_note = relationship("Lead_Notes",back_populates="lead")
    lead_activity = relationship("Lead_Activity",back_populates="lead_")

    Lead_Name = Column(String(255))
    Phone = Column(String(12))
    Email = Column(String(255))

    Owner_ID = Column(Integer,ForeignKey("user.User_ID"))
    leads = relationship("User",back_populates="owner")

    Value = Column(DECIMAL)
    Notes=Column(Text)

    Source_ID = Column(Integer,ForeignKey("sources.Source_ID"))
    lead_source = relationship("Sources",back_populates="source")

    Status_ID = Column(Integer,ForeignKey("status.Status_ID"))
    lead_status = relationship("Status",back_populates="status") 

    Stage_ID = Column(Integer,ForeignKey("stage.Stage_ID"))
    lead_stage = relationship("Stage",back_populates="stage") 

    Priority_ID = Column(Integer,ForeignKey("priority.Priority_ID"))
    lead_priority = relationship("Priority",back_populates="priority") 

    Last_Contacted = Column(DateTime)

    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())









