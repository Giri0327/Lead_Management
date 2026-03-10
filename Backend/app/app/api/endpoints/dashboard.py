from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import session
from app.db import get_db,session
from app.crud.dashboard_crud import Dashboard
from app.crud.Lead_crud import Updateleadd, ViewLeadByID,Create
from app.crud.Follow_up_crud import Createfollowup
from app.schema import *
from app.schema.Lead_Schema import Updatelead


router = APIRouter(prefix="/Dashboard", tags=["Dashboard"])


@router.post("/")
async def dash_board(db:session=Depends(get_db)):
    crud=Dashboard(db)
    return crud.total_lead()

