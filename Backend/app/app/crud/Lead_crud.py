from ast import Not
from hmac import new
from sqlalchemy import or_
from fastapi import HTTPException

from app.models import Lead, User, Sources, Stage, Status, Priority
from sqlalchemy.orm import joinedload


class Create:
    def __init__(self, leads, db):
        self.leads = leads
        self.db = db

    # ADD NEW LEAD

    def create_lead(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]

        new_lead = Lead(
            Lead_Name=self.leads.Lead_Name,
            Phone=self.leads.Phone,
            Email=self.leads.Email,
            Owner_ID=self.leads.Owner_ID,
            Value=self.leads.Value,
            Status_ID=self.leads.Status_ID,
            Notes=self.leads.Notes,
            Source_ID=self.leads.Source_ID,
            Stage_ID=self.leads.Stage_ID,
            Priority_ID=self.leads.Priority_ID,
            Company_Name=self.leads.Company_Name,
        )

        if new_lead and role != 1:
            new_lead = new_lead.filter(User.User_ID == current_id)

        self.db.add(new_lead)
        self.db.commit()
        self.db.refresh(new_lead)
        return {"message": "Lead created successfully", "Lead_ID": new_lead.Lead_ID}

        # else:
        #     raise HTTPException(status_code=403,
        #         detail="You are not authorized to perform this action")

    def view_owner(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]

        query = self.db.query(User.User_ID, User.Username)

        if role != 1:
            query = query.filter(User.User_ID == current_id).all()

        results = query

        # return query

        return [row._asdict() for row in results]

    # VIEW ALL LEADS

    def view_lead(self, current_user, limit, offset):
        current_id = current_user["user_id"]
        role = current_user["role"]

        query = (
            self.db.query(
                Lead.Lead_ID,
                Lead.Lead_Name.label("lead_name"),
                Lead.Company_Name.label("company"),
                Lead.Email,
                Lead.Phone,
                User.Username.label("owner"),
                Lead.Value,
                Sources.Source_Name,
                Stage.Stage_Name,
                Status.Status_Name,
                Priority.Priority_Name,
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
            .join(Status, Lead.Status_ID == Status.Status_ID)
            .join(User, Lead.Owner_ID == User.User_ID)
            .join(Sources, Lead.Source_ID == Sources.Source_ID)
        )

        if role != 1:
            query = query.filter(Lead.Owner_ID == current_id)

        results = query.order_by(Lead.Lead_ID.asc()).offset(offset).limit(limit).all()
        return [row._asdict() for row in results]


# UPDATE LEAD


class Updateleadd:
    def __init__(self, db, lead):
        self.db = db
        self.lead = lead

    def update_lead(self):
        self.db.query(Lead).filter(Lead.Lead_ID == self.lead.lead_id).update(
            {
                "Status_ID": self.lead.status_id,
                "Stage_ID": self.lead.stage_id,
                "Priority_ID": self.lead.priority_id,
            }
        )
        self.db.commit()
        return "updated successfully"


# VIEW LEAD BY ID


class ViewLeadByID:
    def __init__(self, db, lead_id):
        self.db = db
        self.lead_id = lead_id

    def view_lead_by_id(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]
        results = (
            self.db.query(
                Lead.Lead_Name.label("lead_name"),
                Lead.Company_Name.label("company"),
                Lead.Email,
                Lead.Phone,
                User.Username.label("owner"),
                Lead.Value,
                Sources.Source_Name,
                Stage.Stage_Name,
                Status.Status_Name,
                Priority.Priority_Name,
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
            .join(Status, Lead.Status_ID == Status.Status_ID)
            .join(User, Lead.Owner_ID == User.User_ID)
            .join(Sources, Lead.Source_ID == Sources.Source_ID)
            #.filter(Lead.Lead_ID == self.lead_id, Lead.Owner_ID == current_id)
        )#.all()

        if role!=1:
             results=results.filter(Lead.Owner_ID==current_id,Lead.Lead_ID==self.lead_id)

        return results.first()


class LeadSearch:
    def __init__(self, db):
        self.db = db

    def search_lead(self, input, current_user, limit, offset):
        user_id = current_user["user_id"]
        role = current_user["role"]

        query = self.db.query(Lead).filter(
            or_(
                Lead.Lead_Name.ilike(f"%{input}%"),
                Lead.Company_Name.ilike(f"%{input}%"),
                Lead.Email.ilike(f"%{input}%"),
            )
        )

        if role != 1:
            query = query.filter(Lead.Owner_ID == user_id)

        results = query.order_by(Lead.Lead_ID.asc()).offset(offset).limit(limit).all()
        return results
