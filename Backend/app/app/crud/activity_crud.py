from fastapi import HTTPException
from app.models import Lead_Activity
from app.models.Lead_Table import Lead
from app.models.User_Table import User
from app.models.Lead_Sources_Table import Sources
from app.models.File_Activity_Table import Activity_file
from fastapi import UploadFile, File, Depends
import cloudinary.uploader
from app.core.security import cloudinary
from sqlalchemy import func


class Activity:

    def __init__(self,activity,db):  
        self.activity=activity
        self.db=db

# ADD ACTIVITY TO LEAD       

    def add_activity(self,user_id):

            activity = Lead_Activity(

                Lead_ID = self.activity.lead_id,
                User_ID = user_id,
                Notes = self.activity.notes,
                Scheduled_On = self.activity.scheduled_on,

            )
            self.db.add(activity)
            self.db.commit()
            self.db.refresh(activity)

            lead = self.db.query(Lead).filter(Lead.Lead_ID == activity.Lead_ID).first()

            if lead:
                lead.Last_Contacted = activity.Created_At
            
            self.db.commit()
            self.db.refresh(activity)

            return {"message":"Activity Added"}

# VIEW ACTIVITIY TIMELINE (NOTES OF COMPLETED ACTIVIITES)

    def view_activity(self,lead_id,current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        query = (self.db.query(
            Lead_Activity.Notes,
            Lead_Activity.Scheduled_On,
            User.Username
        )
        .join(User,Lead_Activity.User_ID == User.User_ID)
        # .filter(Lead_Activity.Lead_ID == lead_id)
        # .order_by(Lead_Activity.Scheduled_On.asc())
        
        )

        if lead_id:
            query=query.filter(Lead_Activity.Lead_ID == lead_id)

        if role!=1:
            query=query.filter(Lead_Activity.User_ID ==current_id)

        result = query.order_by(Lead_Activity.Scheduled_On.asc()).all()

        if not result:
            return {"message":"No Activities!!"}
        
        return result


        # return view_activities

# SHOW RECENT LEAD DETAILS

class Details:
    def __init__(self,activity,db):
        self.db=db
        self.activity=activity
    
    def show_details (self,lead_id):

        query = (self.db.query(

                Lead_Activity.Scheduled_On,
                Lead.Last_Contacted,
                Sources.Source_Name,
                Lead.Notes

            )
            .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)
            .join(Sources,Lead.Source_ID == Sources.Source_ID)
            .filter(Lead.Lead_ID == lead_id)
            .order_by(Lead_Activity.Scheduled_On.desc())
            .first())

        return query

       
class Files:

    def __init__(self, activity_id, user_id,activity, db):
        self.db = db
        self.activity_id = activity_id
        self.user_id = user_id
        self.activity = activity

# ADD FILE IF NEEDED FOR AN ACTIVITY

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
                detail="Only PDF, JPG, JPEG, PNG, PPTX and XLSX files are allowed"
            )
        
        # dbuser = self.db.query(User).filter(
                #     User.User_ID == self.user_id
        filename = file.filename.split(".")[0]
        extension = file.filename.split(".")[1]

        result = cloudinary.uploader.upload(
            file.file,
            public_id=filename,
            format=extension
        )

        print(result)

        version = result["version"]
        public_id = result["public_id"]

        url = f"https://res.cloudinary.com/dedavidqu/image/upload/v{version}/{public_id}.{extension}"

  
        short_url = url.replace(
            "https://res.cloudinary.com/dedavidqu/image/upload/",
            "CLOUDINARY/"
        )

        print(short_url)

        file_data = Activity_file(
            Activity_ID=self.activity_id,
            File_url=short_url   
        )

        self.db.add(file_data)
        self.db.commit()
        self.db.refresh(file_data)

        return {
            "message": "File Added",
            "file_Name": filename,
            "file_URL": url  
        }

# VIEW FILES AVAILABLE IN AN ACTIVITY

    def view_file(self,activity_id,current_user):

        current_id = current_user["user_id"]
        role = current_user["role"]

        query = (self.db.query(
            Activity_file.Activity_file_ID,
            Activity_file.Activity_ID,
            Lead.Lead_Name,
            Activity_file.File_url
        )
        .join(Lead_Activity, Activity_file.Activity_ID == Lead_Activity.Activity_ID)
        .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID))
        # .filter(Activity_file.Activity_ID == self.activity_id)
        # .all())
        if activity_id:
                query= query.filter(Lead_Activity.Activity_ID==activity_id)
        if role !=1:
                query=query.filter(Lead_Activity.User_ID==current_id)

        query = query.all()
        return query
     
# # VIEW RECENT ACTIVITY IN DASHBOARD PAGE

#     def view_recent_files(self,current_user):

#         current_id = current_user["user_id"]
#         role = current_user["role"]

#         query = (
#             self.db.query(
#                 Lead_Activity.Notes,
#                 Lead.Lead_Name,               
#             )
#             .join(Lead, Lead_Activity.Lead_ID == Lead.Lead_ID)
#         )

#         if role!=1:
#              query=query.filter(Lead_Activity.User_ID==current_id)

#         result = query.order_by(Lead_Activity.Scheduled_On.desc()).all()


#         return result
            

