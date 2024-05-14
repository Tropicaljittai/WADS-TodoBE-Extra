from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

def get_todo_id(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if todo:
        return todo
    else: raise HTTPException(status_code=404, detail="Todo doesn't exist")

def get_todo_title(db: Session, title: str):
    todo = db.query(models.Todo).filter(models.Todo.title == title).first()
    if todo:
        return todo
    else: raise HTTPException(status_code=404, detail="Todo doesn't exist")

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    todo = db.query(models.Todo).offset(skip).limit(limit).all()
    if todo:
        return todo
    else: raise HTTPException(status_code=404, detail="All todos is done!")

def create_todo(db: Session, task: schemas.Todo):
    db_task = models.Todo(title = task.title, completed = task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_todo_id(db: Session, id: int):
    task = get_todo_id(db, id)
    if task:
        db.delete(task)
        db.commit()
        return {"message":"Todo sucesfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="Todo doesn't exist")

def delete_todo_title(db: Session, title: str):
    task = get_todo_title(db, title)
    if task:
        db.delete(task)
        db.commit()
        return {"message":"Todo successfuly deleted"}
    else:
        raise HTTPException(status_code=404, detail="Todo doesn't exist")
    
def delete_all_todos(db: Session):
    if db.query(models.Todo).delete():
        db.commit()
        return {"message":"Todo sucessfuly deleted"}
    else:
        raise HTTPException(status_code=404, detail="All todos is done") 

def update_todo(db: Session, task_id: int, todo_update: schemas.TodoUpdate):
    db_todo = get_todo_id(db, task_id)
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo doesn't exist")
    
    for field, value in todo_update.model_dump().items():
        setattr(db_todo, field, value)
    
    db.commit()
    
    return {"message" : "Todo successfuly updated"}