from fastapi import APIRouter, Depends, HTTPException
from app.db import session,get_db

from app.schema import Stage
from app.crud import create_Stage,view_all_Stage,update_Stage,delete_Stage

router = APIRouter(prefix="/lead", tags=["Stage"])

@router.post("/create_Stage")
def stage_create(user:Stage,db:session=Depends(get_db)):
    return create_Stage(user,db)

@router.get("/view_Stage")
def view_stage(db:session=Depends(get_db)):
    return view_all_Stage(db)

@router.put("/update_Stage")
def update_stage_name(stage_id:int,user:Stage,db:session=Depends(get_db)):
    return update_Stage(stage_id,user,db)

@router.delete("/stage_Delete")
def stage_delete(stage_id:int,db:session=Depends(get_db)):
    return delete_Stage(stage_id,db)