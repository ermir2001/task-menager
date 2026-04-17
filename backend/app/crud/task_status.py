from sqlalchemy.orm import Session

from app.models.task_status import TaskStatus


def get_task_statuses(db: Session):
    return db.query(TaskStatus).all()


def get_task_status(db: Session, status_id: int):
    return db.query(TaskStatus).filter(TaskStatus.id == status_id).first()