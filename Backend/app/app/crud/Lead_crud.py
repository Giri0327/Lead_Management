from app.models.Lead_Table import Lead

from app.models.Lead_Table import Lead

class Create:
    def __init__(self, lead, db):
        self.lead = lead
        self.db = db

    def create_lead(self):
        new_lead = Lead(
            Lead_Name=self.lead.lead_name,
            Phone=self.lead.phone,
            Email=self.lead.email,
            #Owner_ID=self.lead.owner_id,
            Value=self.lead.value,
            #Status_ID=self.lead.status_id,
            Notes=self.lead.notes,
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


class View:
    def __init__(self, db):
        self.db = db

    def view_lead(self):
        leads = self.db.query(Lead).all()
        return leads