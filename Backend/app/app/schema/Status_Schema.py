from pydantic import BaseModel


class Status(BaseModel):
    status_name: str
