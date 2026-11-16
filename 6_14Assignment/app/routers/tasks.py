# project/starter/app/routers/tasks.py
# Module 5 Project — Task endpoints (auth-scoped)
#
# TODO: Implement full task CRUD, all endpoints protected by get_current_user
# All queries must filter by current_user.id (users can only see their own tasks)

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.task import TaskCreate, TaskPatch, TaskResponse
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.auth import get_current_user
router = APIRouter()


# TODO: POST /tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = Task(
        **task.model_dump(),
        owner_id=current_user.id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# TODO: GET /tasks
@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.owner_id == current_user.id
    ).all()

    return tasks

# TODO: GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return task

# TODO: PATCH /tasks/{task_id}
@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task_data: TaskPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# TODO: DELETE /tasks/{task_id}
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted successfully"}


# TODO: GET /tasks/{task_id}/suggest
@router.get("/{task_id}/suggest")
def suggest_task_action(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Placeholder endpoint for AI-powered task suggestions.
    TODO: Return a mock suggestion dict.
    """

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "task_id": task.id,
        "suggestion": "Break this task into smaller steps to make it easier to complete."
    }