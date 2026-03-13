from fastapi import APIRouter, Depends
from app.db import session,get_db
from app.crud import create_Source,view_all_Source,update_Source,delete_Source
from app.schema import Lead_Source
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Source"])


@router.post("/create_Source")
async def Source_create(user:Lead_Source,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return create_Source(user,db)

@router.get("/view_Source")
async def view_Source(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    return view_all_Source(db)

@router.put("/update_Source")
async def update_Source_name(source_id:int,user:Lead_Source,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return update_Source(source_id,user,db)

@router.delete("/Source_Delete")
async def Source_delete(source_id:int,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    return delete_Source(source_id,db)