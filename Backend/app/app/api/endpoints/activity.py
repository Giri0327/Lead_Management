from fastapi import APIRouter, Depends, File,  UploadFile
from app.db import get_db,session
from app.crud import Activity,Details,Files
from app.schema.Lead_Activites_Schema import Lead_Activity
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Activity"])


@router.post("/add_Activity")
async def create_activity(activity:Lead_Activity,current_user = Depends(role_required([2])),db:session=Depends(get_db)):
    creator = Activity(activity, db)
    new_lead = creator.add_activity(current_user["user_id"])
    return new_lead

@router.get("/view_Activity")
async def get_activity(lead_id:int,current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    creator = Activity(lead_id, db)
    view_lead = creator.view_activity(lead_id)
    return view_lead


@router.get("/activity_Details")
async def activity_Details(lead_id:int,current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    creator = Details(lead_id, db)
    view_details = creator.show_details(lead_id)
    return view_details

@router.post("/add_File")
async def create_File(activity_id:int,current_user = Depends(role_required([2])),db:session=Depends(get_db),file: UploadFile = File(...)):
    creator = Files(activity_id,None,None,db)
    new_lead = creator.add_file(current_user["user_id"],file)
    return new_lead

@router.get("/view_Files")
async def view_Files(activity_id:int,current_user = Depends(role_required([1,2])),db:session=Depends(get_db)):
    creator = Files(activity_id,None,None, db)
    view_file = creator.view_file()
    return view_file

# @router.get("/view_all_lead_Notes")
# def view_all_Notes(user_id:int,db:session=Depends(get_db)):
#     creator = Files(user_id,None,None, db)
#     view_all_file = creator.view_recent_files()
#     return view_all_file

@router.get("/view_all_lead_notes")
async def view_all_notes(user_id: int,current_user = Depends(role_required([1,2])), db: session = Depends(get_db)):
    creator = Files(None, user_id, None, db)
    return creator.view_recent_files()