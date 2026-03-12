from fastapi import APIRouter, Depends
from app.db import session,get_db
from app.crud import create_status, delete_status, update_status, view_all_status
from app.schema import Status
from app.api.deps import get_current_user,role_required

router = APIRouter(prefix="/lead", tags=["Status"])


@router.post("/create_Status")
async def status_create(user:Status,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return create_status(user,db)

@router.get("/view_Status")
async def view_status(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    return view_all_status(db)

@router.put("/update_Status")
async def update_status_name(status_id:int,user:Status,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return update_status(status_id,user,db)

@router.delete("/status_Delete")
async def status_delete(status_id:int,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return delete_status(status_id,db)