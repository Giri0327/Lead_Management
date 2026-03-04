from pydantic import BaseModel

class Lead_Activity(BaseModel):
    user_id:int
    note:str
