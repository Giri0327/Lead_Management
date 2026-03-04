from pydantic import BaseModel

class Stage(BaseModel):
    stage_id:int
    stage_name:str
    