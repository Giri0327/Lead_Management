from fastapi import APIRouter, Depends
from app.db import session, get_db
from app.crud import SourceCRUD
from app.schema import Lead_Source
from app.api.deps import role_required

router = APIRouter(prefix="/lead", tags=["Source"])

# CREATE SOURCE


@router.post("/create_Source")
async def Source_create(
    user: Lead_Source,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    source = SourceCRUD(user, db)
    new_source = source.create_Source()
    return new_source


# VIEW ALL SOURCE


@router.get("/view_Source")
async def view_Source(
    current_user=Depends(role_required([1, 2])), db: session = Depends(get_db)
):
    source = SourceCRUD(None, db)
    new_source = source.view_all_Source()
    return new_source


# UPDATE SOURCE


@router.put("/update_Source")
async def update_Source_name(
    source_id: int,
    user: Lead_Source,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    source = SourceCRUD(source_id, user, db)
    new_source = source.update_Source()
    return new_source


# DELETE PRIORITY


@router.delete("/Source_Delete")
async def Source_delete(
    source_id: int,
    current_user=Depends(role_required([1])),
    db: session = Depends(get_db),
):
    source = SourceCRUD(source_id, db)
    new_source = source.delete_Source()
    return new_source
