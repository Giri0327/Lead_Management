from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.salespipeline_crud import Salespipeline
from app.schema import *

router = APIRouter(prefix="/salespipeline", tags=["salespipeline"])

@router.post("/count")
def salespipeline(db: Session = Depends(get_db)):
    try:
        count=salespipeline(db)
        return count.salespipeline_count()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))