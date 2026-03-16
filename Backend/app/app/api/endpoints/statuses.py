from fastapi import APIRouter, Depends
from app.db import session,get_db
from app.crud import StatusCRUD
from app.schema import Status
from app.api.deps import get_current_user,role_required

router = APIRouter(prefix="/lead", tags=["Status"])

# CREATE STATUS

@router.post("/create_Status")
async def status_create(user:Status,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    status = StatusCRUD(user,db)
    new_status = status.create_status()
    return new_status

# VIEW STATUS

@router.get("/view_Status")
async def view_status(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    # return view_all_status(db)
    status = StatusCRUD(None,db)
    new_status = status.view_all_status()
    return new_status

# UPDATE STATUS

@router.put("/update_Status")
async def update_status_name(status_id:int,user:Status,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    status = StatusCRUD(status_id,user,db)
    new_status = status.update_status()
    return new_status

# DELETE STATUS

@router.delete("/status_Delete")
async def status_delete(status_id:int,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    status = StatusCRUD(status_id,db)
    new_status = status.delete_status()
    return new_status