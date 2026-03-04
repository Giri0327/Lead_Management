from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from app.db import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Roles(Base):

    __tablename__ = "roles"

    Role_ID = Column(Integer,primary_key=True)

    Role_Name = Column(String(255))
    roles = relationship("User",back_populates="role_id_user")
    Created_At= Column(DateTime,server_default=func.now())
    Updated_At=Column(DateTime,server_default=func.now(),onupdate=func.now())

