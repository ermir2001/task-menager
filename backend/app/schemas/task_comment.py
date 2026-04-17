from pydantic import BaseModel, Field
from app.schemas.user import UserResponse
from datetime import datetime

class TaskCommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class TaskCommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)

class TaskCommentResponse(BaseModel):
    id: int
    task_id: int
    content: str
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True