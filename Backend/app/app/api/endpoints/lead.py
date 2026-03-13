from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import session
from app.db import get_db,session
from app.crud import Create
from app.crud.Lead_crud import Updateleadd, ViewLeadByID,Create
from app.crud.Follow_up_crud import Createfollowup
from app.schema import *
from app.schema.Lead_Schema import Updatelead
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Lead"])

@router.post("/create")
async def add_lead(leads: Leads,current_user = Depends(role_required([2])), db: session = Depends(get_db)):
    try:
        creator = Create(leads, db)
        new_lead = creator.create_lead()

        return new_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/show")
async def view_lead(page:int, size: int,current_user = Depends(role_required([1,2])),db: session = Depends(get_db)):
    try:
        all_leads = Create(None,db)
        offset = (page - 1) * size
        return all_leads.view_lead(limit=size, offset=offset)
    except Exception as e:
        return e

@router.put("/update")
async def update_lead(leadupdate:Updatelead,current_user = Depends(role_required([2])),db:session = Depends(get_db)):
    data=Updateleadd(db,leadupdate)
    return data.update_lead()


@router.get("/view/{lead_id}")
async def view_lead_by_id(lead_id: int,current_user = Depends(role_required([1])), db: session = Depends(get_db)):
    lead=ViewLeadByID(db, lead_id)
    return lead.view_lead_by_id()


@router.post("/schedule-followup")
async def followup_schedule(followup:Follow_up_schedule,current_user = Depends(role_required([2])),db:session=Depends(get_db)):
        creator = Createfollowup(None,followup, db)
        new_followup = creator.schedule_followup()
        return new_followup

@router.get("/next_followup")
async def next_followup(lead_id:int,current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
        creator = Createfollowup(lead_id,None,db)
        upcoming_followup = creator.get_next_followup(lead_id)
        return upcoming_followup
    

@router.get("/upcoming_followups")
async def upcoming_followups(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
        creator = Createfollowup(None,None,db)
        upcoming_followup = creator.view_upcoming_followups()
        return upcoming_followup
    

@router.get("/this_week_followups")
async def this_week_followups(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
        creator = Createfollowup(None,None,db)
        this_week_followup = creator.view_this_week_followups()
        return this_week_followup
    

@router.post("/updating_followups")
async def update_followups(followup_id:int,followup:Follow_up_schedule,current_user = Depends(role_required([2])),db:session=Depends(get_db)):
        creator = Createfollowup(followup_id,followup,db)
        update_followup = creator.update_followup(followup_id)
        return update_followup
    
@router.get("/track_followups")
async def trackfollowup(current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
     creator = Createfollowup(None,None,db)
     track = creator.track_followups()
     return track