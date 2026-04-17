from pydantic import BaseModel


class TaskPriorityBase(BaseModel):
    name: str


class TaskPriorityCreate(TaskPriorityBase):
    pass


class TaskPriorityResponse(TaskPriorityBase):
    id: int

    class Config:
        from_attributes = True