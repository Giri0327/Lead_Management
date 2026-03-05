from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.Lead_crud import Create
from app.schema.Lead_Schema import Leads

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/")
def add_lead(lead: Leads, db: Session = Depends(get_db)):
    try:
        creator = Create(lead, db)
        new_lead = creator.create_lead()
        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))