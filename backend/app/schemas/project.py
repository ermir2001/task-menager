from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(max_length = 100)
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    author_id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True