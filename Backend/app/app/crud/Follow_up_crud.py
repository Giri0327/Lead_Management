# from sqlalchemy.orm import relationship

# class Follow_Up(Base):

#     __tablename__ = "follow_up"

#     Follow_Up_ID = Column(Integer,primary_key=True)

#     User_ID  = Column(Integer,ForeignKey("user.User_ID",ondelete = "CASCADE")) #FK
#     user = relationship("User",back_populates = "follow_ups")

#     Lead_ID = Column(Integer,ForeignKey("lead_data.Lead_ID"))
#     lead_id = relationship("Lead",back_populates = "lead")

#     Contact_Type = Column(String(255),nullable = False)
#     Notes = Column(Text)
#     Contacted_On = Column(DateTime)

#     Created_At= Column(DateTime,server_default = func.now())

from fastapi import HTTPException

from app.models import Lead,Follow_Up

class Create:
    def __init__(self, followup, db):
        self.followup = followup
        self.db = db
    
    def schedule_followup(self):

        lead = self.db.query(Lead).filter(Lead.Lead_ID == self.followup.lead_id).first()

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        new_followup = Follow_Up(
            User_ID = self.followup.user_id,
            Lead_ID = self.followup.lead_id,
            Notes = self.followup.notes,
            Contact_Type = self.followup.contact_type,
            Contacted_On = self.followup.contacted_on,
            Status = self.followup.status
        )
        self.db.add(new_followup)
        self.db.commit()
        self.db.refresh(new_followup)

        return {"message":"Follow-up scheduled!"}
    
