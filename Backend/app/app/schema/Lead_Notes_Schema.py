from pydantic import BaseModel

class Lead_Notes(BaseModel):
    lead_id:int
    user_id:int
    notes:str

