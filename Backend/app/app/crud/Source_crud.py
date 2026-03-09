from fastapi import HTTPException
from requests import Session

from app.schema import *
from app.models import *


def create_Source(user,db:Session):
        new_Source = Sources(
        Source_Name=user.source_name
    )
        db.add(new_Source)
        db.commit()
        db.refresh(new_Source)
        return {"Source Created succesfully"}

def view_all_Source(db:Session):
        dbuser=db.query(Sources).all()
        return dbuser

def update_Source(source_id:int,user,db:Session):
        dbuser=db.query(Sources).filter(Sources.Source_ID==source_id).first()
        if not dbuser:
            raise HTTPException(status_code=404,
                                detail="Invalid User")
        dbuser.Source_Name=user.source_name
        db.commit()
        db.refresh(dbuser)
        return {"message":"Source Updated Succesfully!!"}

def delete_Source(source_id:int,db:Session):
       dbuser = db.query(Sources).filter(Sources.Source_ID==source_id).first()
       if not dbuser:
              raise HTTPException(status_code=404,detail="User not Found!!")
       db.delete(dbuser)
       db.commit()
       return {"message":"Source Deleted succesfully!!"}

                

        
        


        