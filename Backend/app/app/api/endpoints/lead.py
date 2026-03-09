from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import session
from app.db import get_db,session
from app.crud import Create
from app.crud.Lead_crud import Updateleadd
from app.schema import *
from app.schema.Lead_Schema import Updatelead

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/create")
def add_lead(leads: Leads, db: session = Depends(get_db)):
    try:
        creator = Create(leads, db)
        new_lead = creator.create_lead()
        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/show")
def view_lead(page:int, size: int,db: session = Depends(get_db)):
    all_leads = Create(None, db)
    offset = (page - 1) * size
    return all_leads.view_lead(limit=size, offset=offset)

@router.put("/update")
def update_lead(leadupdate:Updatelead,db:session = Depends(get_db)):
    data=Updateleadd(db,leadupdate)
    return data.update_lead()