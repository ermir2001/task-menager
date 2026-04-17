from sqlalchemy.orm import Session

from app.models.task_comment import TaskComment
from app.schemas.task_comment import TaskCommentCreate, TaskCommentUpdate


def get_task_comments(db: Session, task_id: int):
    return (
        db.query(TaskComment)
        .filter(TaskComment.task_id == task_id)
        .order_by(TaskComment.created_at.asc())
        .all()
    )


def get_task_comment(db: Session, comment_id: int):
    return (
        db.query(TaskComment)
        .filter(TaskComment.id == comment_id)
        .first()
    )


def create_task_comment(
    db: Session,
    comment_data: TaskCommentCreate,
    task_id: int,
    user_id: int,
):
    new_comment = TaskComment(
        content=comment_data.content,
        task_id=task_id,
        user_id=user_id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def update_task_comment(
    db: Session,
    comment: TaskComment,
    comment_data: TaskCommentUpdate,
):
    if comment_data.content is not None:
        comment.content = comment_data.content

    db.commit()
    db.refresh(comment)
    return comment


def delete_task_comment(db: Session, comment: TaskComment):
    db.delete(comment)
    db.commit()