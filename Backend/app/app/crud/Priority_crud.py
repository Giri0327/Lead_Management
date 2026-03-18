from fastapi import HTTPException
from app.models import Priority
from app.db import session


class PriorityCRUD:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    # CREATE NEW PRIORITY

    def create_Priority(self):
        new_Priority = Priority(Priority_Name=self.user.priority_name)
        self.db.add(new_Priority)
        self.db.commit()
        self.db.refresh(new_Priority)

        return {"Priority Created succesfully"}

    # VIEW ALL PRIORITY

    def view_all_Priority(self):

        dbuser = self.db.query(Priority).all()
        return dbuser

    # UPDATE PRIORITY

    def update_Priority(self, priority_id: int):

        dbuser = (
            self.db.query(Priority).filter(Priority.Priority_ID == priority_id).first()
        )
        if not dbuser:
            raise HTTPException(status=404, detail="Invalid User")
        dbuser.Priority_Name = self.user.priority_name
        self.db.commit()
        self.db.refresh(dbuser)
        return {"message": "Priority Updated Succesfully!!"}

    # DELETE PRIORITY

    def delete_Priority(self, priority_id: int):
        dbuser = (
            self.db.query(Priority).filter(Priority.Priority_ID == priority_id).first()
        )
        if not dbuser:
            raise HTTPException(status=404, detail="User not Found!!")
        self.db.delete(dbuser)
        self.db.commit()
        return {"message": "Priority Deleted succesfully!!"}
