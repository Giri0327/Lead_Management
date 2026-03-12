from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import session
from app.db import get_db,session
from app.crud.dashboard_crud import Dashboard
from app.crud.Lead_crud import Updateleadd, ViewLeadByID,Create
from app.crud.Follow_up_crud import Createfollowup
from app.schema import *
from app.schema.Lead_Schema import Updatelead
from app.api.deps import role_required


router = APIRouter(prefix="/Dashboard", tags=["Dashboard"])


@router.post("/")
async def dash_board(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    crud=Dashboard(db)
    return crud.total_lead()
@router.post("/Recentleads")
async def recent_lead(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    recent=Dashboard(db)
    return recent.recentlead()
@router.post("/Pipeline_by_Stage")
async def pipeline_by_stage(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    pipe=Dashboard(db)
    return pipe.Pipeline_by_stage()

@router.post("/Lead_Distribution")
async def distribution(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    pipe=Dashboard(db)
    return pipe.Lead_distribution()



@router.post("/graph")
async def graph_(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    pipe=Dashboard(db)
    return pipe.graph()


