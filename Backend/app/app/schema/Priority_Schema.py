from pydantic import BaseModel

class Priority(BaseModel):
    priority_id:int
    priority_name:set
    