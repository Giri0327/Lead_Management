from app.models.Lead_Table import Lead

class Creat:
    def __init__(self,lead,db):
        self.lead = lead
        self.db = db

    def create_lead(self):
        new_lead = Lead(
            Lead_name=self.lead.lead_name,
            Phone=self.lead.phone,
            Email=self.lead.email,
            Owner_id=self.lead.owner_id,
            Value=self.lead.value,
            status_id=self.lead.status_id,
            notes=self.lead.notes,
            Source_id=self.lead.source_id,
            Stage_id=self.lead.stage_id,
            Priority=self.lead.priority_id
            )
        self.db.add(new_lead)
        self.db.commit()
        self.db.refresh(new_lead)
        if new_lead is not None:   
            return "User created successfully"  
        
        
from app.models.Lead_Table import Lead

class Create:
    def __init__(self, lead, db):
        self.lead = lead
        self.db = db

    def create_lead(self):
        # Map Pydantic snake_case fields to SQLAlchemy PascalCase columns
        field_mapping = {
            "lead_name": "Lead_Name",
            "phone": "Phone",
            "email": "Email",
            "owner_id": "Owner_ID",
            "value": "Value",
            "status_id": "Status_ID",
            "notes": "Notes",
            "source_id": "Source_ID",
            "stage_id": "Stage_ID",
            "priority_id": "Priority_ID"
        }

        # Build dictionary for SQLAlchemy model
        lead_data = {field_mapping[k]: v for k, v in self.lead.dict().items()}

        # Create Lead instance
        new_lead = Lead(**lead_data)

        # Add to DB
        self.db.add(new_lead)
        self.db.commit()
        self.db.refresh(new_lead)  # Refresh to get Lead_ID and timestamps

        return new_lead