from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import session
from app.db import get_db,session
from app.crud import Create
from app.crud.Lead_crud import Updateleadd
from app.schema import *
from app.schema.Lead_Schema import Updatelead

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/")
def add_lead(lead: Leads, db: session = Depends(get_db)):
    try:
        creator = Create(lead, db)
        new_lead = creator.create_lead()
        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/view_leads")
def view_lead(db: session = Depends(get_db)):
    all_leads = Create(None, db)
    return all_leads.view_lead()

@router.put("/Update Lead")
def update_lead(leadupdate:Updatelead):
    data=Updateleadd(db,leadupdate)
    return data.update_lead()