from datetime import datetime
from pydantic import BaseModel

class Follow_ups(BaseModel):
    user_id:int
    lead_id:int
    contact_type:str
    notes:str
    

class Follow_up_schedule(BaseModel):
    user_id:int
    lead_id:int
    notes:str
    contact_type:str
    contacted_on:datetime
    status:bool
    