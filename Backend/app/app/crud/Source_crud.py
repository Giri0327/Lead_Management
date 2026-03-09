from fastapi import HTTPException
from app.models import Sources
from app.db import session


def create_Source(user,db:session):
        new_Source = Sources(
        Source_Name=user.source_name
    )
        db.add(new_Source)
        db.commit()
        db.refresh(new_Source)
        return {"Source Created succesfully"}

def view_all_Source(db:session):
        dbuser=db.query(Sources).all()
        return dbuser

def update_Source(source_id:int,user,db:session):
        dbuser=db.query(Sources).filter(Sources.Source_ID==source_id).first()
        if not dbuser:
            raise HTTPException(status_code=404,
                                detail="Invalid User")
        dbuser.Source_Name=user.source_name
        db.commit()
        db.refresh(dbuser)
        return {"message":"Source Updated Succesfully!!"}

def delete_Source(source_id:int,db:session):
       dbuser = db.query(Sources).filter(Sources.Source_ID==source_id).first()
       if not dbuser:
              raise HTTPException(status_code=404,detail="User not Found!!")
       db.delete(dbuser)
       db.commit()
       return {"message":"Source Deleted succesfully!!"}

                

        
        


        