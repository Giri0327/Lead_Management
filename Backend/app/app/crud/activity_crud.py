from fastapi import HTTPException
from app.models import Lead_Activity,Lead_Sources_Table,File_Activity_Table
from app.models.Lead_Table import Lead
from app.models.User_Table import User
from app.models.Lead_Sources_Table import Sources
from app.models.File_Activity_Table import Activity_file
from fastapi import APIRouter, UploadFile, File, Depends
import cloudinary.uploader
from app.core.security import cloudinary
from sqlalchemy import func


class Activity:
    def __init__(self,activity,db):
        self.activity=activity
        self.db=db

# ADD ACTIVITY TO LEAD        

    def add_activity(self,lead_id):

        dbuser = self.db.query(Lead_Activity).filter(Lead_Activity.Lead_ID==lead_id).first()
        
        if dbuser:

            activity = Lead_Activity(

                Lead_ID = self.activity.lead_id,
                User_ID = self.activity.user_id,
                Notes = self.activity.notes,
                Scheduled_On = self.activity.scheduled_on,

            )
            self.db.add(activity)

            lead = self.db.query(Lead).filter(Lead.Lead_ID == activity.Lead_ID).first()

            if lead:
                lead.Last_Contacted = activity.Scheduled_On

            self.db.commit()
            self.db.refresh(activity)

            return {"message":"Activity Added"}

#VIEW ACTIVITIES 


    def view_activity(self):

        view_activities = (self.db.query(
            Lead_Activity.Notes,
            Lead_Activity.Scheduled_On,
            User.Username
        )
        .join(User,Lead_Activity.User_ID == User.User_ID)
        .order_by(Lead_Activity.Scheduled_On.asc())
        .all()
        )
        return view_activities


class Details:
    def __init__(self,activity,db):
        self.db=db
        self.activity=activity
    
    def show_details (self,lead_id):

        dbuser = self.db.query(Lead_Activity).filter(Lead_Activity.Lead_ID==lead_id).first()
        
        if dbuser:

            details = (self.db.query(

                Lead_Activity.Scheduled_On,
                Lead.Last_Contacted,
                Sources.Source_Name,
                Lead.Notes

            )
            .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)
            .join(Sources,Lead.Source_ID == Sources.Source_ID)
            .filter(Lead.Lead_ID == lead_id)
            .order_by(Lead_Activity.Scheduled_On.desc())
            .all())

            return details

class Files:

    def __init__(self, activity_id, user_id,activity, db):
        self.db = db
        self.activity_id = activity_id
        self.user_id = user_id
        self.activity = activity

    def add_file(self,current_user,file: UploadFile = File(...)):

        user_id=current_user
        activity = self.db.query(Lead_Activity).filter(
            Lead_Activity.Activity_ID == self.activity_id
        ).first()

        if not activity:
            return {"error": "Activity not found"}
        
        filename = file.filename.lower()

        if not filename.endswith((".pdf", ".jpg", ".jpeg",".png",".pptx",".xlsx")):
            raise HTTPException(
                status_code=400,
                detail="Only PNG and JPEG images are allowed"
            )
        
        # dbuser = self.db.query(User).filter(
        #     User.User_ID == self.user_id
        filename = file.filename.split(".")[0]   # remove extension    LEAD.jpg  [0]=LEAD, [1]=jpg
        extension = file.filename.split(".")[1]

        result = cloudinary.uploader.upload(
            file.file,
            public_id=filename,
            format=extension
        )

        print(result)
        
        file_url = result["secure_url"]

        file = Activity_file(
            Activity_ID = self.activity_id,
            File_url = file_url
        )

        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)

        return {"message": "File Added",
                "file_Name":filename,
                "file_URL":file_url}
    
    def view_file(self):

        activity = self.db.query(Lead_Activity).filter(
            Lead_Activity.Activity_ID == self.activity_id
        ).first()

        if not activity:
            return {"error": "Activity not found"}
        
        viewfile = (self.db.query(
            Activity_file.Activity_file_ID,
            Activity_file.Activity_ID,
            Lead.Lead_Name,
            Activity_file.File_url
        )
        .join(Lead_Activity, Activity_file.Activity_ID == Lead_Activity.Activity_ID)
        .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)
        .filter(Activity_file.Activity_ID == self.activity_id)
        .all())

        return viewfile
     

        # files = self.db.query(Activity_file).filter(
        #     Activity_file.Activity_ID == self.activity_id
        # ).all()

        # print(files)
            
    def view_recent_files(self):

        viewfile = (
            self.db.query(
                Lead_Activity.Notes,
                Lead.Lead_Name,
                
            )
            .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)
            .filter(Lead_Activity.User_ID == self.user_id)
            .order_by(Lead_Activity.Scheduled_On.desc())
            .all()
        )

        return viewfile
            

