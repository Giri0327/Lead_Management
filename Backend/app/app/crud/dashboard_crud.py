import calendar
from app.models.Lead_Table import Lead
from app.models.Lead_Activities_Table import Lead_Activity
from app.models.Stage_Table import Stage
from app.models.Priority_Table import Priority
from sqlalchemy import case, func, and_
from datetime import date, datetime, timedelta
from sqlalchemy import func, case, and_
from datetime import datetime, timedelta
from sqlalchemy import func, case, and_
from datetime import datetime, timedelta

today = date.today()


# DASHBOARD
class Dashboard:
    def __init__(self, db):
        self.db = db

    # VIEW TOTAL LEADS
    def total_leadd(self, current_user):

        today = datetime.today()
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (start + timedelta(days=32)).replace(day=1)
        prev_month_end = start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        # COUNT OF TOTAL LEADS

        # totallead=self.db.query(func.count(Lead.Lead_ID)).scalar()

        # CURRENT MONTH LEAD COUNT

        current_month_leads = (
            self.db.query(func.count(Lead.Lead_ID))
            .filter(Lead.Created_At >= start, Lead.Created_At < next_month)
            .scalar()
        )

        # PREVIOUS MONTH LEAD COUNT

        previous_month_leads = (
            self.db.query(func.count(Lead.Lead_ID))
            .filter(Lead.Created_At >= prev_month_start, Lead.Created_At < start)
            .scalar()
        )

        # IF prev_month = 0, current_month = 20, vs_last_month = 100% INCREASE
        # IF prev_month = 0, current_month = 0, vs_last_month = 0% INCREASE

        if previous_month_leads == 0:
            vs_last_month = 100 if current_month_leads > 0 else 0
        else:
            vs_last_month = (
                (current_month_leads - previous_month_leads) / previous_month_leads
            ) * 100

        vs_last_month = round(vs_last_month, 2)

        # COUNT OF LEADS EXCEPT STAGE 5 (WON) AND STAGE 6 (LOST)

        Active_opportunities = (
            self.db.query(func.count(Lead.Lead_ID).label("Active_opportunities"))
            .filter(and_(Lead.Stage_ID != 5, Lead.Stage_ID != 6))
            .first()
        )

        # RATE CHANGE OF QUALIFIED PER MONTH

        this_month_Conversion_rate = (
            self.db.query(func.count(Lead.Lead_ID))
            .filter(
                and_(
                    Lead.Status_ID == 3,  # STATUS_ID 3 = QUALIFIED
                    Lead.Created_At >= start,
                    Lead.Created_At < next_month,
                )
            )
            .scalar()
        )

        last_month_Conversion_rate = (
            self.db.query(func.count(Lead.Lead_ID))
            .filter(
                and_(
                    Lead.Status_ID == 3,
                    Lead.Created_At >= prev_month_start,
                    Lead.Created_At < start,
                )
            )
            .scalar()
        )

        if last_month_Conversion_rate == 0:
            Conversion_ = 100 if this_month_Conversion_rate > 0 else 0
        else:
            Conversion_ = (
                (this_month_Conversion_rate - last_month_Conversion_rate)
                / last_month_Conversion_rate
            ) * 100

        Conversion_percent_vs_last_month = round(Conversion_, 2)

        # Conversion_rate=(self.db.query(func.count(Lead.Lead_ID))
        #                 .filter(Lead.Status_ID==3)).scalar()
        # precentage=(Conversion_rate/totallead)*100

        if current_month_leads:
            percentage = round(
                (this_month_Conversion_rate / current_month_leads) * 100, 1
            )
        else:
            percentage = 0

        # NEW LEADS TODAY

        New_leads_today = (
            (self.db.query(func.count(Lead.Lead_ID)))
            .filter(Lead.Stage_ID == 1, func.date(Lead.Created_At) == today)
            .scalar()
        )

        # HIGH PRIORITY LEADS (PRIORITY_ID = 1 = HIGH)

        high_priority = (
            self.db.query(func.count(Lead.Lead_ID).label("Lead_count"))
            .filter(Lead.Priority_ID == 1)
            .first()
        )

        # TOTAL PIPELINE VALUE (AMOUNT)

        total_pipeline_value = (
            self.db.query(func.sum(Lead.Value).label("Total_Pipeline_Value"))
        ).first()

        return [
            {
                "title": "Total Leads",
                "value": current_month_leads,
                "percent_vs_last_month": vs_last_month,
            },
            {
                "title": "Leads in Pipeline",
                "value": Active_opportunities.Active_opportunities,
            },
            {
                "title": "Conversion Rate",
                "value": percentage,
                "percent_vs_last_month": Conversion_percent_vs_last_month,
            },
            {"title": "New Leads Today", "value": New_leads_today},
            {"title": "High Priority", "value": high_priority.Lead_count},
            {
                "title": "Total Pipeline Value",
                "value": total_pipeline_value.Total_Pipeline_Value,
            },
        ]

    def total_lead(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]

        today = datetime.today()
        today_date = today.date()

        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (start + timedelta(days=32)).replace(day=1)

        prev_month_end = start - timedelta(days=1)
        prev_month_start = prev_month_end.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        stats = self.db.query(
            # Current month leads
            func.sum(
                case(
                    (and_(Lead.Created_At >= start, Lead.Created_At < next_month), 1),
                    else_=0,
                )
            ).label("current_month_leads"),
            # Previous month leads
            func.sum(
                case(
                    (
                        and_(
                            Lead.Created_At >= prev_month_start, Lead.Created_At < start
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("previous_month_leads"),
            # Active opportunities
            func.sum(case((~Lead.Stage_ID.in_([5, 6]), 1), else_=0)).label(
                "active_opportunities"
            ),
            # Qualified this month
            func.sum(
                case(
                    (
                        and_(
                            Lead.Status_ID == 3,
                            Lead.Created_At >= start,
                            Lead.Created_At < next_month,
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("qualified_this_month"),
            # Qualified last month
            func.sum(
                case(
                    (
                        and_(
                            Lead.Status_ID == 3,
                            Lead.Created_At >= prev_month_start,
                            Lead.Created_At < start,
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("qualified_last_month"),
            # New leads today
            func.sum(
                case(
                    (
                        and_(
                            Lead.Stage_ID == 1, func.date(Lead.Created_At) == today_date
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("new_leads_today"),
            # High priority
            func.sum(case((Lead.Priority_ID == 1, 1), else_=0)).label("high_priority"),
            # Total pipeline value
            func.sum(Lead.Value).label("total_pipeline_value"),
        )  # .first()

        if role != 1:
            stats = stats.filter(Lead.Owner_ID == current_id)

        stats = stats.first()

        current_month_leads = stats.current_month_leads or 0
        previous_month_leads = stats.previous_month_leads or 0

        if previous_month_leads == 0:
            vs_last_month = 100 if current_month_leads > 0 else 0
        else:
            vs_last_month = (
                (current_month_leads - previous_month_leads) / previous_month_leads
            ) * 100

        vs_last_month = round(vs_last_month, 2)

        qualified_this_month = stats.qualified_this_month or 0
        qualified_last_month = stats.qualified_last_month or 0

        if qualified_last_month == 0:
            Conversion_ = 100 if qualified_this_month > 0 else 0
        else:
            Conversion_ = (
                (qualified_this_month - qualified_last_month) / qualified_last_month
            ) * 100

        Conversion_percent_vs_last_month = round(Conversion_, 2)

        if current_month_leads:
            percentage = round((qualified_this_month / current_month_leads) * 100, 1)
        else:
            percentage = 0

        return [
            {
                "title": "Total Leads",
                "value": current_month_leads,
                "percent_vs_last_month": vs_last_month,
            },
            {"title": "Leads in Pipeline", "value": stats.active_opportunities or 0},
            {
                "title": "Conversion Rate",
                "value": percentage,
                "percent_vs_last_month": Conversion_percent_vs_last_month,
            },
            {"title": "New Leads Today", "value": stats.new_leads_today or 0},
            {"title": "High Priority", "value": stats.high_priority or 0},
            {"title": "Total Pipeline Value", "value": stats.total_pipeline_value or 0},
        ]

    # RECENT LEADS

    def recentlead(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]
        recentlead = (
            self.db.query(
                Lead.Lead_ID,
                Lead.Lead_Name,
                Lead.Company_Name,
                Stage.Stage_Name,
                Priority.Priority_Name,
            )
            .join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            .join(Priority, Lead.Priority_ID == Priority.Priority_ID)
        )
        # .order_by(Lead.Created_At.desc())).limit(5).all()

        if role != 1:
            recentlead = recentlead.filter(Lead.Owner_ID == current_id)

        result = (recentlead.order_by(Lead.Created_At.desc())).limit(5).all()

        # return recentleads
        return result

    # VIEW RECENT ACTIVITY IN DASHBOARD PAGE

    def view_recent_files(self, current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        query = self.db.query(
            Lead_Activity.Notes,
            Lead.Lead_Name,
        ).join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)

        if role != 1:
            query = query.filter(Lead_Activity.User_ID == current_id)

        result = query.order_by(Lead_Activity.Scheduled_On.desc()).all()

        return result

    # COUNT OF STAGE (BAR CHART)

    def Pipeline_by_stage(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]
        query = (
            self.db.query(
                # Stage.Stage_ID.label("stage_ID"),
                Stage.Stage_Name.label("stage_name"),
                func.count(Lead.Stage_ID).label("lead_count"),
                # func.sum(Lead.Value).label("total_value")
            ).join(Stage, Lead.Stage_ID == Stage.Stage_ID)
            # .group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()
        )
        if role != 1:
            query = query.filter(Lead.Owner_ID == current_id)

        query = query.group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()

        return query

    # PERCENT OF STAGE (PIE CHART)

    def Lead_distribution(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]
        query = self.db.query(
            Stage.Stage_Name.label("stage_name"),
            func.count(Lead.Stage_ID).label("lead_count"),
        ).join(Stage, Lead.Stage_ID == Stage.Stage_ID)
        # .group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all())
        totallead = self.db.query(func.count(Lead.Lead_ID))  # .scalar()

        if role != 1:
            query = query.filter(Lead.Owner_ID == current_id)
            totallead = totallead.filter(Lead.Owner_ID == current_id)

        query = query.group_by(Lead.Stage_ID).order_by(Stage.Stage_ID.asc()).all()
        totallead = totallead.scalar()

        result = []
        for row in query:
            perc = int(round((row.lead_count / totallead) * 100, 1)) if totallead else 0
            result.append(
                {
                    "stage_name": row.stage_name,
                    # "lead_count": row.lead_count,
                    "percentage": perc,
                }
            )

        return result

    # LINE CHART (TOTAL LEADS AND WON DEALS PER MONTH)

    def graph(self, current_user):
        current_id = current_user["user_id"]
        role = current_user["role"]

        year = datetime.now().year
        start = datetime(year, 1, 1, 0, 0, 0)
        end = datetime(year, 12, 31, 23, 59, 59)

        # TOTAL LEADS PER MONTH

        query = (
            self.db.query(
                func.month(Lead.Created_At).label("month"),
                func.count(Lead.Lead_ID).label("total_leads"),
            ).filter(Lead.Created_At.between(start, end))
            # .group_by(func.month(Lead.Created_At))
            # .order_by(func.month(Lead.Created_At))
            # .all()
        )
        if role != 1:
            query = query.filter(Lead.Owner_ID == current_id)
        query = (
            query.group_by(func.month(Lead.Created_At))
            .order_by(func.month(Lead.Created_At))
            .all()
        )

        data = []

        for i in query:
            data.append({"month": calendar.month_name[i[0]], "Total_Count": i[1]})

        # TOTAL WON LEADS PER MONTH

        dbquery = self.db.query(
            func.month(Lead.Updated_At).label("month"), func.count(Lead.Lead_ID)
        ).filter(and_(Lead.Stage_ID == 5, Lead.Updated_At.between(start, end)))
        # .group_by(func.month(Lead.Updated_At))
        # .order_by(func.month(Lead.Updated_At))
        # .all())

        if role != 1:
            dbquery = dbquery.filter(Lead.Owner_ID == current_id)

        dbquery = (
            dbquery.group_by(func.month(Lead.Updated_At))
            .order_by(func.month(Lead.Updated_At))
            .all()
        )

        won_Data = []

        for i in dbquery:
            won_Data.append({"month": calendar.month_name[i[0]], "Total_Count": i[1]})

        return {"Total Leads per Month": data, "Won Leads per month": won_Data}
