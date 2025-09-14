from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..database import SessionLocal
from ..routers.users import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # basic validation: if project_id provided, ensure it exists and belongs to user (or to any if allowed)
    if task_in.project_id:
        project = db.query(models.Project).filter(models.Project.id==task_in.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status or "pending",
        project_id=task_in.project_id,
        owner_id=task_in.assigned_to or current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(project_id: Optional[int] = Query(None), status: Optional[str] = Query(None), assignee: Optional[int] = Query(None), current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(models.Task)
    if project_id:
        q = q.filter(models.Task.project_id==project_id)
    if status:
        q = q.filter(models.Task.status==status)
    if assignee:
        q = q.filter(models.Task.owner_id==assignee)
    # restrict to tasks visible to current user: owned or in user's projects
    q = q.filter((models.Task.owner_id==current_user.id) | (models.Task.project_id.in_([p.id for p in current_user.projects])))
    tasks = q.all()
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # basic permission: must be owner or project owner
    if task.owner_id != current_user.id:
        proj = db.query(models.Project).filter(models.Project.id==task.project_id).first()
        if not proj or proj.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this task")
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_in: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # only assignee or project owner can update
    proj = db.query(models.Project).filter(models.Project.id==task.project_id).first()
    if task.owner_id != current_user.id and (not proj or proj.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    task.title = task_in.title
    task.description = task_in.description
    task.status = task_in.status or task.status
    task.project_id = task_in.project_id or task.project_id
    task.owner_id = task_in.assigned_to or task.owner_id
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    proj = db.query(models.Project).filter(models.Project.id==task.project_id).first()
    if task.owner_id != current_user.id and (not proj or proj.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    db.delete(task)
    db.commit()
    return