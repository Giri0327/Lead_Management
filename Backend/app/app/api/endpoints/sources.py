from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import *
from app.schema import *


router = APIRouter(prefix="/lead", tags=["Source"])


@router.post("/create_Source")
def Source_create(user:Lead_Source,db:Session=Depends(get_db)):
    return create_Source(user,db)

@router.get("/view_Source")
def view_Source(db:Session=Depends(get_db)):
    return view_all_Source(db)

@router.put("/update_Source")
def update_Source_name(source_id:int,user:Lead_Source,db:Session=Depends(get_db)):
    return update_Source(source_id,user,db)

@router.delete("/Source_Delete")
def Source_delete(source_id:int,db:Session=Depends(get_db)):
    return delete_Source(source_id,db)