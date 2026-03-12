from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from app.db import session,get_db
from app.schema.Priority_Schema import Priority
from app.crud.Priority_crud import create_Priority,view_all_Priority,update_Priority,delete_Priority
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Priority"])

@router.post("/create_Priority")
async def priority_create(user:Priority,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return create_Priority(user,db)

@router.get("/view_Priority")
async def view_priority(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    return view_all_Priority(db)

@router.put("/update_Priority")
async def update_priority_name(priority_id:int,user:Priority,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return update_Priority(priority_id,user,db)

@router.delete("/priority_Delete")
async def priority_delete(priority_id:int,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return delete_Priority(priority_id,db)