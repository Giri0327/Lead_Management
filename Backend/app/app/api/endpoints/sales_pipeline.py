from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud.salespipeline_crud import Salespipeline
from app.schema import *
from app.api.deps import role_required

router = APIRouter(prefix="/salespipeline", tags=["salespipeline"])

@router.post("/count")
async def salespipeline(current_user = Depends(role_required([1,2])),db: Session = Depends(get_db)):
    try:
        data=Salespipeline(db)
        return data.salespipeline_count()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/view")
def sale(current_user = Depends(role_required([2])),db: Session = Depends(get_db)):
    try:
        data=Salespipeline(db)
        return data.pipe()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
async def sale(current_user = Depends(role_required([1,2])),db: Session = Depends(get_db)):
    data=Salespipeline(db)
    return data.pipe()
