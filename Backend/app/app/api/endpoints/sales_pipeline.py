from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.salespipeline_crud import Salespipeline
from app.schema import *
from app.api.endpoints.deps import get_current_user

router = APIRouter(prefix="/salespipeline", tags=["salespipeline"])

@router.post("/count")
def salespipeline(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    try:
        data=Salespipeline(db)
        return data.salespipeline_count()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/view")
def sale(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    data=Salespipeline(db)
    return data.pipe()
