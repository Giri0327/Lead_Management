#from token import PERCENT

import re

from app.models.Lead_Table import Lead
from app.models.Stage_Table import Stage
from app.models.Priority_Table import Priority
from sqlalchemy import func,or_,and_
from datetime import date, datetime,timedelta

today = date.today()

class Dashboard:
    def __init__(self,db):
        self.db=db

    def total_lead(self):
        totallead=self.db.query(func.count(Lead.Lead_ID)).scalar()

        high_priority=self.db.query(func.count(
            Lead.Lead_ID).label("Lead_count")).filter(Lead.Priority_ID==1).first()

        total_pipeline_value=(
            self.db.query(func.sum(Lead.Value).label("Total_Pipeline_Value"))).first()

        Active_opportunities = (
            self.db.query(func.count(Lead.Lead_ID).label("Active_opportunities"))
            .filter(and_(Lead.Source_ID != 5, Lead.Source_ID != 6)).first())
        

        Conversion_rate=(self.db.query(func.count(Lead.Lead_ID))
                        .filter(Lead.Status_ID==3)).scalar()
        #precentage=(Conversion_rate/totallead)*100
        if totallead:
            percentage = round((Conversion_rate / totallead) * 100, 1)
        else:
            percentage = 0
        
        New_leads_today=(self.db.query(func.count(Lead.Lead_ID))).filter(
            Lead.Stage_ID==1,func.date(Lead.Created_At) == today).scalar()
        
        """start = datetime.combine(today, datetime.min.time())   # 2026-03-11 00:00:00
        end = start + timedelta(days=1)                        # 2026-03-12 00:00:00
        New_leads_today = (
            self.db.query(func.count(Lead.Lead_ID))
            .filter(
                Lead.Stage_ID == 1,
                Lead.Created_At >= start,
                Lead.Created_At < end
            )
            .scalar()
        )"""

        return {"total_leads": totallead,
                "Active_opportunities":Active_opportunities.Active_opportunities,
                "Conversion_rate":f"{percentage}%",
                "New_leads_today":New_leads_today,
                "high_priority_leads": high_priority.Lead_count,
                "total_pipeline_value": total_pipeline_value.Total_Pipeline_Value,
                }
    
    def recentlead(self):
        recentleads=(self.db.query(Lead.Lead_ID,
                                   Lead.Lead_Name,
                                   Lead.Company_Name,
                                   Stage.Stage_Name,
                                   Priority.Priority_Name)
                                   .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
                                   .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
                                   .order_by(Lead.Created_At.desc())).limit(5).all()
        return recentleads
    
    def Pipeline_by_stage(self):
        query = (
            self.db.query(
                #Stage.Stage_ID.label("stage_ID"),
                Stage.Stage_Name.label("stage_name"),
                func.count(Lead.Stage_ID).label("lead_count"),
                #func.sum(Lead.Value).label("total_value")
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()
        )
        return query
    

    def Lead_distribution(self):
        query = (
            self.db.query(
                #Stage.Stage_ID.label("stage_ID"),
                Stage.Stage_Name.label("stage_name"),
                func.count(Lead.Stage_ID).label("lead_count"),
                #func.sum(Lead.Value).label("total_value")
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()
        )
        totallead = self.db.query(func.count(Lead.Lead_ID)).scalar()

        result = []
        for row in query:
            perc = int(round((row.lead_count / totallead) * 100, 1)) if totallead else 0
            result.append({
                "stage_name": row.stage_name,
                #"lead_count": row.lead_count,
                "percentage": perc
            })

        return result

