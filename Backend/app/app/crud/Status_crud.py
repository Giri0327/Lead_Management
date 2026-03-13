from fastapi import HTTPException
from app.models import Status
from app.db import session



def create_status(user,db:session):
        new_status = Status(
        Status_Name=user.status_name
    )
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return {"Status Created succesfully"}

def view_all_status(db:session):
        dbuser=db.query(Status).all()
        return dbuser

def update_status(status_id:int,user,db:session):
        dbuser=db.query(Status).filter(Status.Status_ID==status_id).first()
        if not dbuser:
            raise HTTPException(status_code=404,
                                detail="Invalid User")
        dbuser.Status_Name=user.status_name
        db.commit()
        db.refresh(dbuser)
        return {"message":"Status Updated Succesfully!!"}

def delete_status(status_id:int,db:session):
       dbuser = db.query(Status).filter(Status.Status_ID==status_id).first()
       if not dbuser:
              raise HTTPException(status_code=404,detail="User not Found!!")
       db.delete(dbuser)
       db.commit()
       return {"message":"Status Deleted succesfully!!"}

                

        
        


        