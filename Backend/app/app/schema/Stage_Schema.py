from pydantic import BaseModel


class Stage(BaseModel):
    stage_name: str
