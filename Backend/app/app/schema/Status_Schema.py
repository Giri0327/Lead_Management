from pydantic import BaseModel

class Status(BaseModel):
    status_id:int
    status_name:str