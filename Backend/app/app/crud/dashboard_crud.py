import calendar
from app.models.Lead_Table import Lead
from app.models.Stage_Table import Stage
from app.models.Priority_Table import Priority
from sqlalchemy import func,and_
from datetime import date, datetime,timedelta

today = date.today()

class Dashboard:
    def __init__(self,db):
        self.db=db

    def total_lead(self):
        totallead=self.db.query(func.count(Lead.Lead_ID)).scalar()

        today = datetime.today()
        start = today.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        next_month = (start + timedelta(days=32)).replace(day=1)
        prev_month_end = start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(
            day=1,hour=0,minute=0,second=0, microsecond=0)

        current_month_leads = (self.db.query(func.count(Lead.Lead_ID))
                               .filter(Lead.Created_At >= start,
                                       Lead.Created_At < next_month)
                                       .scalar())
        previous_month_leads = (self.db.query(func.count(Lead.Lead_ID))
                                .filter(Lead.Created_At >= prev_month_start,
                                        Lead.Created_At < start).scalar())

        if previous_month_leads == 0:
            vs_last_month = 100 if current_month_leads > 0 else 0
        else:
            vs_last_month = ((current_month_leads - previous_month_leads
                 ) / previous_month_leads) * 100

        vs_last_month = round(vs_last_month, 2)



        high_priority=self.db.query(func.count(
            Lead.Lead_ID).label("Lead_count")).filter(
                Lead.Priority_ID==1).first()


        total_pipeline_value=(
            self.db.query(func.sum(Lead.Value).label("Total_Pipeline_Value"))
            ).first()


        Active_opportunities = (
            self.db.query(func.count(Lead.Lead_ID)
                          .label("Active_opportunities"))
                          .filter(and_(Lead.Source_ID != 5,
                                       Lead.Source_ID != 6)).first())
        
        

        Conversion_rate=(self.db.query(func.count(Lead.Lead_ID))
                        .filter(Lead.Status_ID==3)).scalar()
        #precentage=(Conversion_rate/totallead)*100
        if totallead:
            percentage = round((Conversion_rate / totallead) * 100, 1)
        else:
            percentage = 0


        this_month_Conversion_rate =(self.db.query(func.count(Lead.Lead_ID))
                                    .filter(and_(Lead.Status_ID == 3,
                                                Lead.Created_At >= start,
                                                Lead.Created_At < next_month
                                                )).scalar())

        last_month_Conversion_rate =(self.db.query(func.count(Lead.Lead_ID))
                                     .filter(and_(
                                         Lead.Status_ID == 3,
                                         Lead.Created_At >= prev_month_start,
                                         Lead.Created_At < start)).scalar())

        if last_month_Conversion_rate == 0:
            Conversion_ = 100 if this_month_Conversion_rate > 0 else 0
        else:
            Conversion_ = ((this_month_Conversion_rate 
                            - last_month_Conversion_rate) 
                            / last_month_Conversion_rate) * 100

        Conversion_percent_vs_last_month = round(Conversion_, 2)

        
        New_leads_today=(self.db.query(func.count(Lead.Lead_ID))).filter(
            Lead.Stage_ID==1,func.date(Lead.Created_At) == today).scalar()
    

        return ({"Title":"Total Leads","total_leads": totallead,
                 "%_vs_last_month":vs_last_month},
                {"Title":"Leads in Pipeline",
                 "Active_opportunities":Active_opportunities.Active_opportunities},
                {"Title":"Conversion Rate",
                 "Conversion_rate":percentage,
                 "Conversion_percent_vs_last_month":Conversion_percent_vs_last_month},
                {"Title":"New Leads Today",
                 "New_leads_today":New_leads_today},
                {"Title":"High Priority",
                 "high_priority_leads": high_priority.Lead_count},
                {"Title":"Total Pipeline Value",
                 "total_pipeline_value": total_pipeline_value.Total_Pipeline_Value})
                  
    
    def recentlead(self):
        recentleads=(self.db
                     .query(Lead.Lead_ID,Lead.Lead_Name,
                            Lead.Company_Name,Stage.Stage_Name,
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
            perc = int(round((row.lead_count / totallead) * 100, 1)
                       ) if totallead else 0
            result.append({
                "stage_name": row.stage_name,
                #"lead_count": row.lead_count,
                "percentage": perc
            })

        return result

    def graph(self):
        year = datetime.now().year
        start = datetime(year, 1, 1, 0, 0, 0)
        end = datetime(year, 12, 31, 23, 59, 59)

        query = (
            self.db.query(
                func.month(Lead.Created_At).label("month"),
                func.count(Lead.Lead_ID).label("total_leads")
            )
            .filter(Lead.Created_At.between(start, end))
            .group_by(func.month(Lead.Created_At))
            .order_by(func.month(Lead.Created_At))
            .all()
        )

        data =[]

        for i in query:
            data.append(
                        {"month": calendar.month_name[i[0]],
                         "Total_Count":i[1]})
        

        dbquery = (self.db.query(
            func.month(Lead.Updated_At).label("month"),
            func.count(Lead.Lead_ID)
        )
        .filter(and_ (Lead.Stage_ID==5,Lead.Updated_At.between(start, end) ))
        .group_by(func.month(Lead.Updated_At))
        .order_by(func.month(Lead.Updated_At))
        .all())
        # return data,dbquery
        won_Data =[]

        for i in dbquery:
            won_Data.append(
                        {"month": calendar.month_name[i[0]],
                         "Total_Count":i[1]})
            
        return {"Total Leads per Month":data,
                "Won Leads per month":won_Data}
    
