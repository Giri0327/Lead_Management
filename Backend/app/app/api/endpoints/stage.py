from fastapi import APIRouter, Depends
from app.db import session, get_db
from app.schema import Stage
from app.crud import StageCRUD
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Stage"])

# CREATE STAGE


@router.post("/create_Stage")
async def stage_create(
    user: Stage, current_user=Depends(role_required([1])), db: session = Depends(get_db)
):
    stage = StageCRUD(user, db)
    new_stage = stage.create_Stage()
    return new_stage


# VIEW STAGE


@router.get("/view_Stage")
async def view_stage(
    current_user=Depends(role_required([1, 2])), db: session = Depends(get_db)
):
    stage = StageCRUD(None, db)
    new_stage = stage.view_all_Stage()
    return new_stage


# UPDATE STAGE


@router.put("/update_Stage")
async def update_stage_name(
    stage_id: int,
    user: Stage,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    # return update_Stage(stage_id,user,db)
    stage = StageCRUD(stage_id, user, db)
    new_stage = stage.update_Stage()
    return new_stage


# DELETE STAGE


@router.delete("/stage_Delete")
async def stage_delete(
    stage_id: int,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    stage = StageCRUD(stage_id, db)
    new_stage = stage.delete_Stage()
    return new_stage
