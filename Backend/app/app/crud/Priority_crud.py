from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schema import Priority_Schema
from app.models import Priority


def create_Priority(user,db:Session):
        new_Priority = Priority(
        Priority_Name=user.priority_name
    )
        db.add(new_Priority)
        db.commit()
        db.refresh(new_Priority)
        return {"Priority Created succesfully"}

def view_all_Priority(db:Session):
        dbuser=db.query(Priority).all()
        return dbuser

def update_Priority(priority_id:int,user,db:Session):
        dbuser=db.query(Priority).filter(Priority.Priority_ID==priority_id).first()
        if not dbuser:
            raise HTTPException(status=404,
                                detail="Invalid User")
        dbuser.Priority_Name=user.priority_name
        db.commit()
        db.refresh(dbuser)
        return {"message":"Priority Updated Succesfully!!"}

def delete_Priority(priority_id:int,db:Session):
       dbuser = db.query(Priority).filter(Priority.Priority_ID==priority_id).first()
       if not dbuser:
              raise HTTPException(status=404,detail="User not Found!!")
       db.delete(dbuser)
       db.commit()
       return {"message":"Priority Deleted succesfully!!"}

                

        
        


        