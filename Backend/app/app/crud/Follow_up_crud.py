from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models import Lead, Follow_Up, User
from sqlalchemy import func


class Createfollowup:

    def __init__(self, lead_id, followup, db):
        self.lead_id = lead_id
        self.followup = followup
        self.db = db

    # ADD FOLLOW UP FOR A LEAD

    def schedule_followup(self, user_id):

        lead = self.db.query(Lead).filter(Lead.Lead_ID == self.followup.lead_id).first()

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        new_followup = Follow_Up(
            User_ID=user_id,
            Lead_ID=self.followup.lead_id,
            Notes=self.followup.notes,
            Contact_Type=self.followup.contact_type,
            Contacted_On=self.followup.contacted_on,
            Status=self.followup.status,
        )
        self.db.add(new_followup)
        self.db.commit()
        self.db.refresh(new_followup)

        return {"message": "Follow-up scheduled!"}

    # NEXT UPCOMING FOLLOWUP FOR A LEAD

    def get_next_followup(self, lead_id: int):

        # current_id = current_user["user_id"]
        # role = current_user["role"]

        followup = (
            self.db.query(
                User.Username,
                Follow_Up.Contact_Type,
                Follow_Up.Contacted_On,
                Follow_Up.Notes,
            )
            .join(User, Follow_Up.User_ID == User.User_ID)
            .filter(Follow_Up.Lead_ID == lead_id)
            .filter(Follow_Up.Contacted_On > datetime.now())
            .filter(Follow_Up.Status == False)
            .order_by(Follow_Up.Contacted_On.asc())
            .first()
        )
        # if role !=1:
        #     query = followup.filter(Follow_Up.User_ID == current_id)
        # result = (
        #     query.order_by(Follow_Up.Contacted_On.asc()).first()
        # )
        if not followup:
            return {"message": "No followup scheduled"}
        return followup

    # ALL UPCOMING FOLLOWUPS FOR A LEAD

    def view_upcoming_followups(self, lead_id, current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        query = (
            self.db.query(
                Lead.Lead_Name,
                Lead.Company_Name,
                Follow_Up.Contact_Type,
                Follow_Up.Contacted_On,
                Follow_Up.Notes,
            )
            .join(Follow_Up, Lead.Lead_ID == Follow_Up.Lead_ID)
            .filter(Follow_Up.Contacted_On > datetime.now())
            # .filter(Follow_Up.Lead_ID == lead_id)
        )

        if lead_id:
            query = query.filter(Follow_Up.Lead_ID == lead_id)

        if role != 1:
            query = query.filter(Follow_Up.User_ID == current_id)

        result = query.order_by(Follow_Up.Contacted_On.asc()).all()

        if not result:
            return {"message": "No upcoming followups"}

        return result

    # THIS WEEK FOLLOWUPS FOR A LEAD

    def view_this_week_followups(self, lead_id, current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        today = datetime.now()

        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        query = (
            self.db.query(
                Lead.Lead_Name,
                Lead.Company_Name,
                Follow_Up.Contact_Type,
                Follow_Up.Contacted_On,
                Follow_Up.Notes,
            )
            .join(Follow_Up, Lead.Lead_ID == Follow_Up.Lead_ID)
            .filter(
                Follow_Up.Contacted_On >= start_of_week,
                Follow_Up.Contacted_On <= end_of_week,
            )
            # .all()
        )

        if lead_id:
            query = query.filter(Follow_Up.Lead_ID == lead_id)

        if role != 1:
            query = query.filter(Follow_Up.User_ID == current_id)
        query = query.order_by(Follow_Up.Contacted_On.asc()).all()

        return query

    # UPDATE FOLLOWUP

    def update_followup(self, followup_id: int):
        leaduser = (
            self.db.query(Follow_Up)
            .filter(Follow_Up.Follow_Up_ID == followup_id)
            .first()
        )

        if not leaduser:
            raise HTTPException(status_code=404, detail="Lead not Found")

        self.db.query(Follow_Up).filter(Follow_Up.Follow_Up_ID == followup_id).update(
            {
                "User_ID": self.followup.user_id,
                "Lead_ID": self.followup.lead_id,
                "Contact_Type": self.followup.contact_type,
                "Notes": self.followup.notes,
                "Contacted_On": self.followup.contacted_on,
                "Status": self.followup.status,
            }
        )
        self.db.commit()
        return {"message": "Updated Successfully!!"}

    # COUNT FOLLOWUPS

    def track_followups(self, lead_id, current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        query = self.db.query(Follow_Up)

        if lead_id:
            query = query.filter(Follow_Up.Lead_ID == lead_id)

        if role != 1:
            query = query.filter(Follow_Up.User_ID == current_id)

        today = datetime.now().date()
        thisweek = today + timedelta(days=7)

        # NO OF FOLLLOW UPS TODAY

        today_count = query.filter(func.date(Follow_Up.Contacted_On) == today).count()

        # NO OF FOLLLOW UPS THIS WEEK

        thisweek_count = query.filter(
            func.date(Follow_Up.Contacted_On).between(today, thisweek)
        ).count()

        # NO OF FOLLLOW UPS OVERDUE (NOT COMPLETED)

        overdue_count = query.filter(
            func.date(Follow_Up.Contacted_On) < today, Follow_Up.Status == False
        ).count()

        # NO OF FOLLLOW UPS COMPLETED

        completed_count = query.filter(
            func.date(Follow_Up.Contacted_On) < today, Follow_Up.Status == True
        ).count()

        return {
            "today_count": today_count,
            "thisweek_count": thisweek_count,
            "overdue_count": overdue_count,
            "completed_count": completed_count,
        }
