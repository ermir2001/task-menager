from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.task_status import get_task_status, get_task_statuses
from app.dependencies import get_current_user, get_db
from app.schemas.task_status import TaskStatusResponse

router = APIRouter(prefix="/task-statuses", tags=["task_statuses"])


@router.get("/", response_model=List[TaskStatusResponse])
def read_task_statuses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_task_statuses(db)


@router.get("/{status_id}", response_model=TaskStatusResponse)
def read_task_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task_status = get_task_status(db, status_id)
    if not task_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status nie istnieje"
        )
    return task_status