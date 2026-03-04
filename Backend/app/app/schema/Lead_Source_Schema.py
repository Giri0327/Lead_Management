from pydantic import BaseModel

class Lead_Source(BaseModel):
    source_id:int
    source_name:str
    