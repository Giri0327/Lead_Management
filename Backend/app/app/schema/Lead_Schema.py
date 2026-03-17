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
    Company_Name: Optional[str]=None
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

class Updatelead(BaseModel):
    lead_id:int
    stage_id:int
    status_id:int
    priority_id:int




'''from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from typing import Optional


class Leads(BaseModel):

    Lead_Name: Optional[str] = Field(None, min_length=2, max_length=100)

    Phone: Optional[str] = Field(
        None,
        pattern=r'^\d{10}$',
        description="Phone number must be 10 digits"
    )

    Email: Optional[EmailStr] = None

    Owner_ID: Optional[int] = Field(None, gt=0)

    Value: Optional[Decimal] = Field(None, ge=0)

    Source_ID: Optional[int] = Field(None, gt=0)

    Notes: Optional[str] = Field(None, max_length=500)

    Status_ID: Optional[int] = Field(None, gt=0)

    Stage_ID: Optional[int] = Field(None, gt=0)

    Priority_ID: Optional[int] = Field(None, gt=0)

    Company_Name: Optional[str] = Field(None, max_length=150)


class LeadResponse(BaseModel):

    Lead_ID: int

    Lead_Name: Optional[str] = None

    Phone: Optional[str] = None

    Email: Optional[EmailStr] = None

    Owner_ID: Optional[int] = None

    Value: Optional[Decimal] = None

    Source_ID: Optional[int] = None

    Notes: Optional[str] = None

    Status_ID: Optional[int] = None

    Stage_ID: Optional[int] = None

    Priority_ID: Optional[int] = None

    Last_Contacted: Optional[datetime] = None

    Created_At: datetime

    Updated_At: datetime

    class Config:
        from_attributes = True   # Pydantic v2 (ORM support)


class Updatelead(BaseModel):

    lead_id: int = Field(gt=0)

    stage_id: int = Field(gt=0)

    status_id: int = Field(gt=0)

    priority_id: int = Field(gt=0)'''    