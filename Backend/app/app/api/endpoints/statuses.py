from fastapi import APIRouter, Depends, HTTPException
from app.db import session,get_db
from app.crud import create_status, delete_status, update_status, view_all_status
from app.schema import Status
from app.api.endpoints.deps import get_current_user

router = APIRouter(prefix="/lead", tags=["Status"])


@router.post("/create_Status")
def status_create(user:Status,current_user = Depends(get_current_user),db:session=Depends(get_db)):
    return create_status(user,db)

@router.get("/view_Status")
def view_status(current_user = Depends(get_current_user),db:session=Depends(get_db)):
    return view_all_status(db)

@router.put("/update_Status")
def update_status_name(status_id:int,user:Status,current_user = Depends(get_current_user),db:session=Depends(get_db)):
    return update_status(status_id,user,db)

@router.delete("/status_Delete")
def status_delete(status_id:int,current_user = Depends(get_current_user),db:session=Depends(get_db)):
    return delete_status(status_id,db)