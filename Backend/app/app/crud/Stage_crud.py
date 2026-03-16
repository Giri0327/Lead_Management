from fastapi import HTTPException
from app.models import Stage
from app.db import session

class StageService:
        def __init__(self):
              pass       
        def create_stage(self,user,db:session):
                new_stage = Stage(
                Stage_Name=user.stage_name
                )
                db.add(new_stage)
                db.commit()
                db.refresh(new_stage)
                return {"message":"Stage Created succesfully"}

        def view_all_stage(self,db:session):
                dbuser=db.query(Stage).all()
                return dbuser

        def update_stage(self,stage_id:int,user,db:session):
                dbuser=db.query(Stage).filter(Stage.Stage_ID==stage_id).first()
                if not dbuser:
                 raise HTTPException(status_code=404,
                                        detail="Stage Not Found")
                dbuser.Stage_Name=user.stage_name
                db.commit()
                db.refresh(dbuser)
                return {"message":"Stage Updated Succesfully!!"}

        def delete_stage(self,stage_id:int,db:session):
                dbuser = db.query(Stage).filter(Stage.Stage_ID==stage_id).first()
                if not dbuser:
                        raise HTTPException(status_code=404,detail="User not Found!!")
                db.delete(dbuser)
                db.commit()
                return {"message":"Stage Deleted succesfully!!"}

                        

                
                


                