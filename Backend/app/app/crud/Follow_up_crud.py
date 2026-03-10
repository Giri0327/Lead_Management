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

from datetime import datetime, timedelta

from fastapi import HTTPException

from app.models import Lead,Follow_Up,User
from sqlalchemy import func

class Createfollowup:
    def __init__(self,lead_id, followup, db):
        self.lead_id = lead_id
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
    
    def get_next_followup(self, lead_id:int):
        
        followup = (
            self.db.query(User.Username,
                          Follow_Up.Contact_Type,
                          Follow_Up.Contacted_On,
                          Follow_Up.Notes)
            .filter(Follow_Up.Lead_ID == lead_id)
            .filter(Follow_Up.Contacted_On > datetime.now())
            .filter(Follow_Up.Status == False)
            .order_by(Follow_Up.Contacted_On.asc())
            .first()
        )

        if not followup:
            return {"message":"No followup scheduled"}

        return followup
    

    def view_upcoming_followups(self):
        view_followups =(
            self.db.query(
                Lead.Lead_Name,
                Lead.Company_Name,
                Follow_Up.Contact_Type,
                Follow_Up.Contacted_On,
                Follow_Up.Notes
            )
        .join(Follow_Up,Lead.Lead_ID ==Follow_Up.Lead_ID)
        .filter(Follow_Up.Contacted_On > datetime.now())
        .all()

        )
        return view_followups
    from datetime import datetime, timedelta

    def view_this_week_followups(self):

        today = datetime.now()

        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        view_followups = (
            self.db.query(
                Lead.Lead_Name,
                Lead.Company_Name,
                Follow_Up.Contact_Type,
                Follow_Up.Contacted_On,
                Follow_Up.Notes
            )
            .join(Follow_Up, Lead.Lead_ID == Follow_Up.Lead_ID)
            .filter(
                Follow_Up.Contacted_On >= start_of_week,
                Follow_Up.Contacted_On <= end_of_week
            )
            .all()
        )

        return view_followups

    def update_followup(self,followup_id:int):
        leaduser = self.db.query(Follow_Up).filter(Follow_Up.Follow_Up_ID==followup_id).first()
    
        if not leaduser:
            raise HTTPException(status_code=404,detail="Lead not Found")
        
        self.db.query(Follow_Up).filter(Follow_Up.Follow_Up_ID==followup_id).update({
            "User_ID" : self.followup.user_id,
            "Lead_ID" : self.followup.lead_id,
            "Contact_Type" : self.followup.contact_type,
            "Notes": self.followup.notes,
            "Contacted_On": self.followup.contacted_on,
            "Status":self.followup.status
            
        })
        self.db.commit()
        return {"message":"Updated Successfully!!"}
    
    def track_followups(self):

        today=datetime.now().date()
        thisweek = today +timedelta(days=7)
       
        today_count = (self.db.query(func.count(Follow_Up.Contacted_On))
            .filter(func.date(Follow_Up.Contacted_On) == today)
            .scalar()
        )

        thisweek_count = (self.db.query(func.count(Follow_Up.Contacted_On))
            .filter(Follow_Up.Contacted_On.between(today, thisweek))
            .scalar()
    )
        overdue_count = (self.db.query(func.count(Follow_Up.Contacted_On))
            .filter(Follow_Up.Contacted_On<today,Follow_Up.Status==False)
            .scalar())
        
        completed_count = (self.db.query(func.count(Follow_Up.Contacted_On))
            .filter(Follow_Up.Contacted_On <today,Follow_Up.Status==True)
            .scalar())
    # today_count = (
    #     self.db.query(func.count(Follow_Up.Contacted_On))
    #     .filter(Follow_Up.Contacted_On == today)
    #     .scalar()
    # )
        return {"today_count":today_count,
                "thisweek_count":thisweek_count,
                "overdue_count":overdue_count,
                "completed_count":completed_count}

        


    
