from pydantic import BaseModel

class Roles(BaseModel):
    role_id:int
    role_name:str