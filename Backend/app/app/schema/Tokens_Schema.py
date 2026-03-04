from pydantic import BaseModel

class Token(BaseModel):
    user_id:int
    token:str
    device_type:str
    