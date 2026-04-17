from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.task_priority import get_task_priorities, get_task_priority
from app.dependencies import get_current_user, get_db
from app.schemas.task_priority import TaskPriorityResponse

router = APIRouter(prefix="/task-priorities", tags=["task_priorities"])


@router.get("/", response_model=List[TaskPriorityResponse])
def read_task_priorities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_task_priorities(db)


@router.get("/{priority_id}", response_model=TaskPriorityResponse)
def read_task_priority(
    priority_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task_priority = get_task_priority(db, priority_id)
    if not task_priority:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Priorytet nie istnieje"
        )
    return task_priority