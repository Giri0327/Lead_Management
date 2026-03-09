from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from app.db import session,get_db
from app.schema.Priority_Schema import Priority
from app.crud.Priority_crud import create_Priority,view_all_Priority,update_Priority,delete_Priority

router = APIRouter(prefix="/lead", tags=["Priority"])

@router.post("/create_Priority")
def priority_create(user:Priority,db:session=Depends(get_db)):
    return create_Priority(user,db)

@router.get("/view_Priority")
def view_priority(db:session=Depends(get_db)):
    return view_all_Priority(db)

@router.put("/update_Priority")
def update_priority_name(priority_id:int,user:Priority,db:session=Depends(get_db)):
    return update_Priority(priority_id,user,db)

@router.delete("/priority_Delete")
def priority_delete(priority_id:int,db:session=Depends(get_db)):
    return delete_Priority(priority_id,db)