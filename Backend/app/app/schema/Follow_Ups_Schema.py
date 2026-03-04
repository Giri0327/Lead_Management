from pydantic import BaseModel

class Follow_ups(BaseModel):
    user_id:int
    lead_id:int
    contact_type:str
    notes:str
    