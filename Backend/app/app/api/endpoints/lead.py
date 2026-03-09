from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import *
from app.schema import *

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/")
def add_lead(lead: Leads, db: Session = Depends(get_db)):
    try:
        creator = Create(lead, db)
        new_lead = creator.create_lead()
        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/view_leads")
def view_lead(db: Session = Depends(get_db)):
    all_leads = Create(None, db)
    return all_leads.view_lead()

# @router.put("/update_lead")
# def update_lead_endpoint(lead_id: int, lead: Leads, db: Session = Depends(get_db)):
#     lead_service = Create(None, db) 
#     return lead_service.update_lead(lead_id, lead)

# @router.put("/update_lead")
# def update_lead_endpoint(lead_id: int, lead: Leads, db: Session = Depends(get_db),response_model =):
#     lead_service = Create(None, db) 
#     updated_lead = lead_service.update_lead(lead_id, lead)
#     return updated_lead