from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.Stage_Schema import Stage
from app.crud.Stage_crud import create_Stage,view_all_Stage,update_Stage,delete_Stage

router = APIRouter(prefix="/lead", tags=["Stage"])

@router.post("/create_Stage")
def stage_create(user:Stage,db:Session=Depends(get_db)):
    return create_Stage(user,db)

@router.get("/view_Stage")
def view_stage(db:Session=Depends(get_db)):
    return view_all_Stage(db)

@router.put("/update_Stage")
def update_stage_name(stage_id:int,user:Stage,db:Session=Depends(get_db)):
    return update_Stage(stage_id,user,db)

@router.delete("/stage_Delete")
def stage_delete(stage_id:int,db:Session=Depends(get_db)):
    return delete_Stage(stage_id,db)