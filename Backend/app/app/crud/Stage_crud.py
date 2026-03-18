from fastapi import HTTPException
from app.models import Stage
from app.db import session


class StageCRUD:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    # CREATE STAGE

    def create_Stage(self):
        new_stage = Stage(Stage_Name=self.user.stage_name)
        self.db.add(new_stage)
        self.db.commit()
        self.db.refresh(new_stage)
        return {"Stage Created succesfully"}

    # VIEW STAGE

    def view_all_Stage(self):
        dbuser = self.db.query(Stage.Stage_ID,Stage.Stage_Name).all()
        return dbuser

    # UPDATE STAGE

    def update_Stage(self, stage_id: int):
        dbuser = self.db.query(Stage).filter(Stage.Stage_ID == stage_id).first()
        if not dbuser:
            raise HTTPException(status_code=404, detail="Invalid Stage")
        dbuser.Stage_Name = self.user.stage_name
        self.db.commit()
        self.db.refresh(dbuser)
        return {"message": "Stage Updated Succesfully!!"}

    # DELETE STAGE

    def delete_Stage(self, stage_id: int):
        dbuser = self.db.query(Stage).filter(Stage.Stage_ID == stage_id).first()
        if not dbuser:
            raise HTTPException(status_code=404, detail="User not Found!!")
        self.db.delete(dbuser)
        self.db.commit()
        return {"message": "Stage Deleted succesfully!!"}
