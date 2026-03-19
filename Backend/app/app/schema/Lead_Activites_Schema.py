from datetime import datetime

from pydantic import BaseModel

class Lead_Activity(BaseModel):
    lead_id:int
    notes:str
    #scheduled_on:datetime
