from sqlalchemy.orm import Session

from app.models.task_priority import TaskPriority


def get_task_priorities(db: Session):
    return db.query(TaskPriority).all()


def get_task_priority(db: Session, priority_id: int):
    return db.query(TaskPriority).filter(TaskPriority.id == priority_id).first()