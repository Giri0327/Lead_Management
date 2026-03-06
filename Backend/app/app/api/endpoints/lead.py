from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.Lead_crud import Create,View
from app.schema.Lead_Schema import Leads
from app.crud.Status_crud import create_status
from app.schema.Status_Schema import Status

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/")
def add_lead(lead: Leads, db: Session = Depends(get_db)):
    try:
        creator = Create(lead, db)
        new_lead = creator.create_lead()
        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/create_status")
def status_create(user:Status,db:Session=Depends(get_db)):
    return create_status(user,db)
@router.get("/view_leads")
def view_lead(db: Session = Depends(get_db)):
    view = View(db)
    return view.view_lead()
