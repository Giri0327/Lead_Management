from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Lead_Activity(Base):

    __tablename__ = "lead_activity"

    Activity_ID = Column(Integer,primary_key=True)
    Lead_ID = Column(Integer,ForeignKey("lead.Lead_ID"))
    lead_ = relationship("Lead",back_populates="lead_activity")

    User_ID = Column(Integer,ForeignKey("user.User_ID"))
    lead_user = relationship("User",back_populates="lead_activity")

    Notes_ID = Column(Integer,ForeignKey("lead_notes.Note_ID"))
    lead_activity_note = relationship("Lead_Notes",back_populates="note")


    Scheduled_On = Column(DateTime)

    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())


