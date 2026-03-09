from app.models import Lead
from fastapi import HTTPException, status

class Create:
    def __init__(self, leads, db):
        self.leads = leads
        self.db = db

    def create_lead(self):
        new_lead = Lead(
            Lead_Name = self.leads.Lead_Name,
            Phone = self.leads.Phone,
            Email = self.leads.Email,
            Owner_ID = self.leads.Owner_ID,
            Value = self.leads.Value,
            Status_ID = self.leads.Status_ID,
            Notes = self.leads.Notes,
            Source_ID = self.leads.Source_ID,
            Stage_ID = self.leads.Stage_ID,
            Priority_ID = self.leads.Priority_ID,
            Company_Name = self.leads.Company_Name
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

class Updateleadd:
    def __init__(self,db,lead):
        self.db=db
        self.lead=lead
    
    def update_lead(self):
        self.db.query(Lead).filter(Lead.Lead_ID==self.lead.lead_id).update({
            "Status_ID" : self.lead.status_id,
            "Stage_ID" : self.lead.stage_id,
            "Priority_ID" : self.lead.priority_id
            
        })
        self.db.commit()
        return "updated successfully"



