from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schema import Stage_Schema
from app.models import Stage


def create_Stage(user,db:Session):
        new_stage = Stage(
        Stage_Name=user.stage_name
    )
        db.add(new_stage)
        db.commit()
        db.refresh(new_stage)
        return {"Stage Created succesfully"}

def view_all_Stage(db:Session):
        dbuser=db.query(Stage).all()
        return dbuser

def update_Stage(stage_id:int,user,db:Session):
        dbuser=db.query(Stage).filter(Stage.Stage_ID==stage_id).first()
        if not dbuser:
            raise HTTPException(status_code=404,
                                detail="Invalid User")
        dbuser.Stage_Name=user.stage_name
        db.commit()
        db.refresh(dbuser)
        return {"message":"Stage Updated Succesfully!!"}

def delete_Stage(stage_id:int,db:Session):
       dbuser = db.query(Stage).filter(Stage.Stage_ID==stage_id).first()
       if not dbuser:
              raise HTTPException(status_code=404,detail="User not Found!!")
       db.delete(dbuser)
       db.commit()
       return {"message":"Stage Deleted succesfully!!"}

                

        
        


        