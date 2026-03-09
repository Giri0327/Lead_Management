from datetime import datetime

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

# class Leads(BaseModel):
#     lead_name:Optional[str] = None
#     phone:Optional[str] = None
#     email:Optional[str] = None
#     owner_id:Optional[int] = None
#     value:Optional[Decimal] = None
#     source_id:Optional[int] = None
#     notes:Optional[str] = None
#     status_id:Optional[int] = None
#     stage_id:Optional[int] = None
#     priority_id:Optional[int] = None

#     class Config:
#         orm_mode = True

class Leads(BaseModel):
    # Lead_ID: int
    Lead_Name: Optional[str]=None
    Phone: Optional[str]=None
    Email: Optional[str]=None
    Owner_ID: Optional[int]=None
    Value: Optional[Decimal]=None
    Source_ID: Optional[int]=None
    Notes: Optional[str]=None
    Status_ID: Optional[int]=None
    Stage_ID: Optional[int]=None
    Priority_ID: Optional[int]=None
    # created_at: datetime
    # updated_at: datetime
    # last_contacted: Optional[datetime]

class LeadResponse(BaseModel):
    Lead_ID: int
    Lead_Name: str=None
    Phone: Optional[str]=None
    Email: Optional[str]=None
    Owner_ID: Optional[int]=None
    Value: Optional[Decimal]=None
    Source_ID: Optional[int]=None
    Notes: Optional[str]=None
    Status_ID: Optional[int]=None
    Stage_ID: Optional[int]=None
    Priority_ID: Optional[int]=None
    Last_Contacted: Optional[datetime]=None
    Created_At: datetime
    Updated_At: datetime

    # class Config:
    #     orm_mode = True