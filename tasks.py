from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import jwt_token
from db_connections import get_db, engine, SessionLocal
from db_models import Tasks, Base
from schemas import Task, ShowUser

router=APIRouter(tags=['Tasks'])


@router.get("/")
def tasks():
    return "Welcome to To-do list"


@router.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db), current_user: ShowUser = Depends(jwt_token.get_current_user)):
    return db.query(Tasks).order_by(Tasks.deadline,Tasks.priority).all()


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_new_task(task: Task, db: Session = Depends(get_db),current_user: ShowUser = Depends(jwt_token.get_current_user)):
    new_task=Tasks(tasks=task.task, ownerId= current_user.userId, taskFlag=task.taskFlag, priority=task.priority, deadline=task.deadline)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.delete("/tasks/{taskId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(taskId: int, db:Session=Depends(get_db),current_user: ShowUser = Depends(jwt_token.get_current_user)):
    task=db.query(Tasks).filter(Tasks.taskId==taskId)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {taskId} not found")
    if current_user.userId != task.first().ownerId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Allowed to delete")
    task.delete()
    db.commit()
    return "Deleted"


@router.get("/tasks/{taskId}")
def get_single_task(taskId:int, db: Session = Depends(get_db), current_user: ShowUser = Depends(jwt_token.get_current_user)):
    task= db.query(Tasks).filter(Tasks.taskId==taskId)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {taskId} not found")
    if current_user.userId != task.first().ownerId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Allowed to access")
    return task.first()


@router.put("/{taskId}")
def update_tasks(taskId: int, tasks: Task, db: Session=Depends(get_db),current_user: ShowUser = Depends(jwt_token.get_current_user)):
    task=db.query(Tasks).filter(Tasks.taskId==taskId)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with {taskId} not found")
    if current_user.userId != task.first().ownerId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Allowed to update")
    task.update({Tasks.tasks:tasks.task,Tasks.taskFlag:tasks.taskFlag,Tasks.priority:tasks.priority,Tasks.deadline:tasks.deadline})
    db.commit()
    return "Updated"
