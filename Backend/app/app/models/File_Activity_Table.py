from sqlalchemy import Column, Integer, ForeignKey, DateTime,String,TEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Activity_file(Base):
    __tablename__ = "activity_file"

    Activity_file_ID = Column(Integer, primary_key=True)
    Activity_ID = Column(Integer, ForeignKey("lead_activity.Activity_ID", ondelete="CASCADE"))
    File_url = Column(TEXT)

    # Relationships
    activity = relationship("Lead_Activity", back_populates="activity_file")

    Created_At = Column(DateTime, server_default=func.now())
