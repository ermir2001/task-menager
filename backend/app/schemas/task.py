from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(max_length=150)
    description: Optional[str] = None
    status_id: int
    project_id: int
    assignee_id: int
    priority_id: int
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    priority_id: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskStatusUpdate(BaseModel):
    status_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    author_id: int
    status_id: int
    project_id: int
    assignee_id: int
    priority_id: int
    created_at: datetime
    due_date: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True