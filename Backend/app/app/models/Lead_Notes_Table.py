from sqlalchemy import Column,Text,String,Integer,DECIMAL,DateTime,ForeignKey,Boolean
from db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Lead_Notes(Base):

    __tablename__ = "lead_notes"

    Note_ID = Column(Integer,primary_key=True)
    note = relationship("Lead_Activity",back_populates="lead_activity_note")

    Lead_ID = Column(Integer,ForeignKey("lead.Lead_ID"))
    lead = relationship("Lead",back_populates="lead_note")

    User_ID = Column(Integer,ForeignKey("user.User_ID"))
    leads_note = relationship("User",back_populates="leads_user_note")

    Note = Column(Text)

    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())
