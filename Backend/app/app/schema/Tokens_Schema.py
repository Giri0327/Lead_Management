from pydantic import BaseModel

class Tokens(BaseModel):
    user_id:int
    token:str
    device_type:str
    