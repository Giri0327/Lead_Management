from sqlalchemy import Column, String, Integer, DateTime
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Priority(Base):

    __tablename__ = "priority"

    Priority_ID = Column(Integer, primary_key=True, autoincrement=True)
    priority = relationship("Lead", back_populates="lead_priority")

    Priority_Name = Column(String(255))

    Created_At = Column(DateTime, server_default=func.now())
    Updated_At = Column(DateTime, server_default=func.now(), onupdate=func.now())
