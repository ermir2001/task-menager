from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.task import get_task
from app.crud.task_comment import (
    create_task_comment,
    delete_task_comment,
    get_task_comment,
    get_task_comments,
    update_task_comment,
)
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.task_comment import (
    TaskCommentCreate,
    TaskCommentResponse,
    TaskCommentUpdate,
)

router = APIRouter(tags=["task_comments"])


@router.get("/tasks/{task_id}/comments", response_model=List[TaskCommentResponse])
def read_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task nie istnieje",
        )

    return get_task_comments(db, task_id)


@router.post(
    "/tasks/{task_id}/comments",
    response_model=TaskCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_task_comment(
    task_id: int,
    comment: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task nie istnieje",
        )

    return create_task_comment(db, comment, task_id, current_user.id)


@router.put("/comments/{comment_id}", response_model=TaskCommentResponse)
def edit_task_comment(
    comment_id: int,
    comment_data: TaskCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = get_task_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Komentarz nie istnieje",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Możesz edytować tylko swój komentarz",
        )

    return update_task_comment(db, comment, comment_data)


@router.delete("/comments/{comment_id}")
def remove_task_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = get_task_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Komentarz nie istnieje",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Możesz usunąć tylko swój komentarz",
        )

    delete_task_comment(db, comment)
    return {"message": "Komentarz usunięty"}