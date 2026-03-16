from fastapi import HTTPException
from app.models import Sources
from app.db import session

class SourceCRUD:
       
        def __init__(self,user,db):
              self.user=user
              self.db=db

# CREATE SOURCE

        def create_Source(self):
                new_Source = Sources(
                Source_Name=self.user.source_name
        )
                self.db.add(new_Source)
                self.db.commit()
                self.db.refresh(new_Source)
                return {"Source Created succesfully"}

# VIEW ALL SOURCE

        def view_all_Source(self):
                dbuser=self.db.query(Sources).all()
                return dbuser
        
# UPDATE SOURCE

        def update_Source(self,source_id:int):
                dbuser=self.db.query(Sources).filter(Sources.Source_ID==source_id).first()
                if not dbuser:
                        raise HTTPException(status_code=404,
                                                detail="Invalid User")
                dbuser.Source_Name=self.user.source_name
                self.db.commit()
                self.db.refresh(dbuser)
                return {"message":"Source Updated Succesfully!!"}

# DELETE SOURCE

        def delete_Source(source_id:int,self):
                dbuser = self.db.query(Sources).filter(Sources.Source_ID==source_id).first()
                if not dbuser:
                        raise HTTPException(status_code=404,detail="User not Found!!")
                self.db.delete(dbuser)
                self.db.commit()
                return {"message":"Source Deleted succesfully!!"}

                        

        
        


        