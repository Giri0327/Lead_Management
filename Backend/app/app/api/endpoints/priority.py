from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from app.db import session, get_db
from app.schema.Priority_Schema import Priority_Schema
from app.crud import PriorityCRUD
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Priority"])

# CREATE NEW PRIORITY


@router.post("/create_Priority")
async def priority_create(
    user: Priority_Schema,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    priority = PriorityCRUD(user, db)
    new_priority = priority.create_Priority()
    return new_priority


# VIEW ALL PRIORITY


@router.get("/view_Priority")
async def view_priority(
    current_user=Depends(role_required([1, 2])), db: session = Depends(get_db)
):
    priority = PriorityCRUD(None, db)
    new_priority = priority.view_all_Priority()
    return new_priority


# UPDATE PRIORITY


@router.put("/update_Priority")
async def update_priority_name(
    priority_id: int,
    user: Priority_Schema,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    priority = PriorityCRUD(priority_id, user, db)
    new_priority = priority.update_Priority()
    return new_priority


# DELETE PRIORITY


@router.delete("/priority_Delete")
async def priority_delete(
    priority_id: int,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    priority = PriorityCRUD(priority_id, db)
    new_priority = priority.delete_Priority()
    return new_priority
