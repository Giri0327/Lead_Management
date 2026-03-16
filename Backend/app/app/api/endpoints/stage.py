from fastapi import APIRouter, Depends
from app.db import session,get_db
from app.schema import Stage
from app.crud import StageService
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Stage"])

@router.post("/create_Stage")
async def stage_create(user:Stage,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    x=StageService()
    return x.create_stage(user,db)

@router.get("/view_Stage")
async def view_stage(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    x=StageService()
    return x.view_all_stage(db)

@router.put("/update_Stage")
async def update_stage_name(stage_id:int,user:Stage,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    x=StageService()
    return x.update_stage(stage_id,user,db)

@router.delete("/stage_Delete")
async def stage_delete(stage_id:int,current_user = Depends(role_required([1])),db:session=Depends(get_db)):
    x=StageService()
    return x.delete_stage(stage_id,db)