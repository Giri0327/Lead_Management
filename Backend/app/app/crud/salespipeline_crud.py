from fastapi import HTTPException
from app.schema import Stage_Schema
from app.models import Stage
from app.models.Lead_Table import Lead
from app.models.Priority_Table import Priority
from app.models.User_Table import User
from sqlalchemy import func
class Salespipeline:
    def __init__(self,db):
        self.db=db
    def salespipeline_count(self):
        query = (
            self.db.query(
                Stage.Stage_Name.label("stage_name"),
                func.count(Lead.Stage_ID).label("lead_count"),
                func.sum(Lead.Value).label("total_value")
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .group_by(Lead.Stage_ID).all()
        )
        return query
    
    def pipe(self):
        results = (
        self.db.query(Lead.Lead_Name.label("lead_name"),
            Priority.Priority_Name.label("priority_name"),
            Lead.Value.label("value"),
            User.Username.label("owner_name"),
            Lead.Company_Name.label("company_name"))
        .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
        .join(User, Lead.Owner_ID == User.User_ID)
        .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
        .all())
        return results
