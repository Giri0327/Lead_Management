from requests import Session

from app.models import *


from fastapi import HTTPException, status

class Create:
    def __init__(self, lead, db):
        self.lead = lead
        self.db = db

    def create_lead(self):
        new_lead = Lead(
            Lead_Name=self.lead.Lead_Name,
            Phone=self.lead.Phone,
            Email=self.lead.Email,
            #Owner_ID=self.lead.owner_id,
            Value=self.lead.Value,
            #Status_ID=self.lead.status_id,
            Notes=self.lead.Notes,
            #Source_ID=self.lead.source_id,
            #Stage_ID=self.lead.stage_id,
            #Priority_ID=self.lead.priority_id
        )

        self.db.add(new_lead)
        self.db.commit()
        self.db.refresh(new_lead)

        if new_lead:
            return {
                "message": "Lead created successfully",
                "Lead_ID": new_lead.Lead_ID
            } 
        
    def view_lead(self):
        lead=self.db.query(Lead).all()
        return lead

