from app.models.Lead_Table import Lead
from sqlalchemy import func

class Dashboard:
    def __init__(self,db):
        self.db=db

    def total_lead(self):
        totallead=self.db.query(func.count(Lead.Lead_ID).label("Lead_count")).first()
        high_priority=self.db.query(func.count(Lead.Lead_ID).label("Lead_count")).filter(Lead.Priority_ID==1).first()
        #total_pipeline_value=self.db.query(func.sum(Lead.Pipeline_Value).label("Total_Pipeline_Value")).first()
        return {"total_leads": totallead.Lead_count, 
                "high_priority_leads": high_priority.Lead_count,
                  #"total_pipeline_value": total_pipeline_value.Total_Pipeline_Value
                  }

