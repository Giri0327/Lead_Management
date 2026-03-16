from ast import Not

from app.models import Lead,User,Sources,Stage,Status,Priority
from sqlalchemy.orm import joinedload

class Create:
    def __init__(self, leads, db):
        self.leads = leads
        self.db = db

# ADD NEW LEAD

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
                "Lead_ID": new_lead.Lead_ID} 
        
    """def view_lead(self,current_user, limit, offset):
        current_id=current_user["user_id"]
        role=current_user["role"]
        print(role)

    
        if  role == 1:
            #query = query.filter(Lead.Owner_ID == current_id)
            query=(self.db.query(
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
            Priority.Priority_Name)
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID,isouter=True)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID,isouter=True)
            .join(Status, Lead.Status_ID == Status.Status_ID,isouter=True)
            .join(User, Lead.Owner_ID == User.User_ID,isouter=True)
            .join(Sources, Lead.Source_ID == Sources.Source_ID,isouter=True)
            .order_by(Lead.Lead_ID.asc())
            .offset(offset)
            .limit(limit)).all()
            return [row._asdict() for row in query]
        else:

            query=(self.db.query(
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
                Priority.Priority_Name).filter(Lead.Owner_ID == current_id)
                .join(Stage, Lead.Stage_ID == Stage.Stage_ID,isouter=True)
                .join(Priority, Lead.Priority_ID == Priority.Priority_ID,isouter=True)
                .join(Status, Lead.Status_ID == Status.Status_ID,isouter=True)
                .join(User, Lead.Owner_ID == User.User_ID,isouter=True)
                .join(Sources, Lead.Source_ID == Sources.Source_ID,isouter=True)
                .order_by(Lead.Lead_ID.asc())
                .offset(offset)
                .limit(limit)).all()
            return [row._asdict() for row in query]"""
    
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
                Priority.Priority_Name)
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
            .join(Status, Lead.Status_ID == Status.Status_ID)
            .join(User, Lead.Owner_ID == User.User_ID)
            .join(Sources, Lead.Source_ID == Sources.Source_ID))
        
        if role != 1:
            query = query.filter(Lead.Owner_ID == current_id)

        results = (
            query.order_by(Lead.Lead_ID.asc()).offset(offset)
            .limit(limit).all()
            )
        return [row._asdict() for row in results]

# UPDATE LEAD

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

# VIEW LEAD BY ID
 
class ViewLeadByID:
    def __init__(self,db,lead_id):
        self.db=db
        self.lead_id=lead_id

    def view_lead_by_id(self):
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
                Priority.Priority_Name
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID).join(Priority, Lead.Priority_ID == Priority.Priority_ID)
            .join(Status, Lead.Status_ID == Status.Status_ID).join(User, Lead.Owner_ID == User.User_ID)
            .join(Sources, Lead.Source_ID == Sources.Source_ID)
            .filter(Lead.Lead_ID == self.lead_id).first() #.one_or_none() # ensures only one record exists
        )
        return results
    
    """def view_lead_by_id(self):
        lead = (
            self.db.query(Lead)
            .options(
                joinedload(Lead.stage),
                joinedload(Lead.status),
                joinedload(Lead.priority),
                joinedload(Lead.source),
                joinedload(Lead.owner)
            )
            .filter(Lead.Lead_ID == self.lead_id)
            .first()
        )
        return {
            "lead_name": lead.Lead_Name,
            "company": lead.Company_Name,
            "email": lead.Email,
            "phone": lead.Phone,
            "owner": lead.owner.Username if lead.owner else None,
            "value": lead.Value,
            "source": lead.source.Source_Name if lead.source else None,
            "stage": lead.stage.Stage_Name if lead.stage else None,
            "status": lead.status.Status_Name if lead.status else None,
            "priority": lead.priority.Priority_Name if lead.priority else None
        }"""


