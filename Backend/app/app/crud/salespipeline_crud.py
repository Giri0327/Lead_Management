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
                Stage.Stage_ID.label("stage_ID"),
                Stage.Stage_Name.label("stage_name"),
                func.count(Lead.Stage_ID).label("lead_count"),
                func.sum(Lead.Value).label("total_value")
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()
        )
        return [row._asdict() for row in query]
    
    def pipe(self):
        results = (
            self.db.query(
                Stage.Stage_ID.label("stage_ID"),
                Stage.Stage_Name.label("stage_name"),
                Lead.Lead_ID.label("lead_id"),
                Lead.Lead_Name.label("lead_name"),
                Lead.Company_Name.label("company_name"),
                Lead.Value.label("value"),
                Priority.Priority_Name.label("priority_name"),
                User.Username.label("owner_name")
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .join(User, Lead.Owner_ID == User.User_ID)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID).order_by(Stage.Stage_ID.asc())
            .all())
        Data = {}
        for row in results:
            #print(row)

            stage_name = row.stage_name
            stage_ID = row.stage_ID
            #print(stage_ID)
            if stage_name not in Data:
                Data[stage_name] = {
                    "stage_id":row.stage_ID,
                    "stage": stage_name,
                    "lead_count": 0,
                    "leads": []
                }

            Data[stage_name]["lead_count"] += 1

            Data[stage_name]["leads"].append({
                "lead_id": row.lead_id,
                "lead_name": row.lead_name,
                "company_name": row.company_name,
                "value": row.value,
                "priority": row.priority_name,
                "owner": row.owner_name
            })
        return list(Data.values())