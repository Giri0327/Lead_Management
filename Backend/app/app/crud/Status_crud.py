from fastapi import HTTPException
from app.models import Status
from app.db import session


class StatusCRUD:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    # CREATE STATUS

    def create_status(self):
        new_status = Status(Status_Name=self.user.status_name)
        self.db.add(new_status)
        self.db.commit()
        self.db.refresh(new_status)
        return {"Status Created succesfully"}

    # VIEW ALL STATUS

    def view_all_status(self):
        dbuser = self.db.query(Status.Status_ID,Status.Status_Name).all()
        return dbuser

    # UPDATE STATUS

    def update_status(self, status_id):
        dbuser = self.db.query(Status).filter(Status.Status_ID == status_id).first()
        if not dbuser:
            raise HTTPException(status_code=404, detail="Invalid User")
        dbuser.Status_Name = self.user.status_name
        self.db.commit()
        self.db.refresh(dbuser)
        return {"message": "Status Updated Succesfully!!"}

    # DELETE STATUS

    def delete_status(self, status_id: int):
        dbuser = self.db.query(Status).filter(Status.Status_ID == status_id).first()
        if not dbuser:
            raise HTTPException(status_code=404, detail="User not Found!!")
        self.db.delete(dbuser)
        self.db.commit()
        return {"message": "Status Deleted succesfully!!"}
