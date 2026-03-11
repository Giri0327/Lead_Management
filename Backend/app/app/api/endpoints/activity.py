from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db,session
from app.crud import Activity,Details,Files
from app.schema.Lead_Activites_Schema import Lead_Activity
from app.schema.File_Activity_Schema import File_Activity

router = APIRouter(prefix="/lead", tags=["Activity"])


@router.post("/add_Activity")
def create_activity(activity:Lead_Activity,db:session=Depends(get_db)):
    creator = Activity(activity, db)
    new_lead = creator.add_activity()
    return new_lead

@router.get("/view_Activity")
def get_activity(lead_id:int,db:session=Depends(get_db)):
    creator = Activity(lead_id, db)
    view_lead = creator.view_activity()
    return view_lead


@router.get("/activity_Details")
def activity_Details(lead_id:int,db:session=Depends(get_db)):
    creator = Details(lead_id, db)
    view_details = creator.show_details(lead_id)
    return view_details

@router.post("/add_File")
def create_File(activity_id:int,activity:File_Activity,db:session=Depends(get_db)):
    creator = Files(activity_id,None,activity,db)
    new_lead = creator.add_file()
    return new_lead

@router.get("/view_Files")
def view_Files(activity_id:int,db:session=Depends(get_db)):
    creator = Files(activity_id,None,None, db)
    view_file = creator.view_file()
    return view_file

# @router.get("/view_all_lead_Notes")
# def view_all_Notes(user_id:int,db:session=Depends(get_db)):
#     creator = Files(user_id,None,None, db)
#     view_all_file = creator.view_recent_files()
#     return view_all_file

@router.get("/view_all_lead_notes")
def view_all_notes(user_id: int, db: session = Depends(get_db)):
    creator = Files(None, user_id, None, db)
    return creator.view_recent_files()