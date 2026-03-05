from pydantic import BaseModel
from decimal import Decimal
class Leads(BaseModel):
    lead_name:str
    phone:str
    email:str
    owner_id:int
    value:Decimal
    source_id:int
    notes:str
    status_id:int
    stage_id:int
    priority_id:int