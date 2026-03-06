from requests import Session

from app.schema import Status_Schema
from app.models import Status


def create_status(user,db:Session):
        new_status = Status(
        Status_Name=user.status_name
    )
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return {"User Created succesfully"}