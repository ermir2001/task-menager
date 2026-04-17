from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from app.database import Base


class TaskPriority(Base):
    __tablename__ = "task_priorities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)

    tasks = relationship("Task", back_populates="priority")