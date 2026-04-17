from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate


def create_task(db: Session, task: TaskCreate, author_id: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        author_id=author_id,
        assignee_id=task.assignee_id,
        status_id=task.status_id,
        priority_id=task.priority_id,
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(
            Task.id == task_id,
            or_(
                Task.author_id == user_id,
                Task.assignee_id == user_id
            )
        ).first()


def get_tasks(db: Session, user_id: int, filter_by: str = "all"):
    query = db.query(Task)
    
    if filter_by == "created":
        query = query.filter(Task.author_id == user_id)
    elif filter_by == "assigned":
        query = query.filter(Task.assignee_id == user_id)
    else:
        query = query.filter(
            or_(
                Task.author_id == user_id,
                Task.assignee_id == user_id
                )
            )
    return query.all()



def update_task_by_author(db: Session, db_task: Task, task_data: TaskUpdate):

    if task_data.title is not None:
        db_task.title = task_data.title
    if task_data.description is not None:
        db_task.description = task_data.description
    if task_data.status_id is not None:
        db_task.status_id = task_data.status_id
    if task_data.project_id is not None:
        db_task.project_id = task_data.project_id
    if task_data.assignee_id is not None:
        db_task.assignee_id = task_data.assignee_id
    if task_data.priority_id is not None:
        db_task.priority_id = task_data.priority_id 
    if task_data.due_date is not None:
        db_task.due_date = task_data.due_date 

    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status_by_assignee(db: Session, db_task: Task, status_data: TaskStatusUpdate):
    db_task.status_id = status_data.status_id
    db.commit()
    db.refresh(db_task)
    return db_task



def delete_task(db: Session, db_task: Task):
    db.delete(db_task)
    db.commit()
    return db_task