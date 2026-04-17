from pydantic import BaseModel


class TaskStatusBase(BaseModel):
    name: str


class TaskStatusCreate(TaskStatusBase):
    pass


class TaskStatusResponse(TaskStatusBase):
    id: int

    class Config:
        from_attributes = True