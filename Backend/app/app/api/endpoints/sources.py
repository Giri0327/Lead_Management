from fastapi import APIRouter, Depends, HTTPException
from app.db import session,get_db
from app.crud import create_Source,view_all_Source,update_Source,delete_Source
from app.schema import Lead_Source


router = APIRouter(prefix="/lead", tags=["Source"])


@router.post("/create_Source")
def Source_create(user:Lead_Source,db:session=Depends(get_db)):
    return create_Source(user,db)

@router.get("/view_Source")
def view_Source(db:session=Depends(get_db)):
    return view_all_Source(db)

@router.put("/update_Source")
def update_Source_name(source_id:int,user:Lead_Source,db:session=Depends(get_db)):
    return update_Source(source_id,user,db)

@router.delete("/Source_Delete")
def Source_delete(source_id:int,db:session=Depends(get_db)):
    return delete_Source(source_id,db)