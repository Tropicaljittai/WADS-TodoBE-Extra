from fastapi import FastAPI, HTTPException, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
import crud, models, schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas import Todo

app = FastAPI()
models.Base.metadata.create_all(bind = engine)
origins = [
    "http://localhost:5173",
    "localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/createTask")
def create_task(todo: Todo, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.get("/getTaskID/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    return crud.get_todo_id(db, task_id)

@app.get("/getTaskTitle/{title}")
def get_task_by_title(title: str, db: Session = Depends(get_db)):
    filtered_tasks = crud.get_todo_title(db, title)
    if filtered_tasks:
        return filtered_tasks
    else:
        return {"error": f"No tasks found with title '{title}'"}
    
@app.get("/getAllTasks")
def get_all_tasks(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.put("/updateTask/{task_id}")
def update_task(task_id: int, task_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_todo(db, task_id, task_update)
    return updated_task

@app.delete("/deleteTaskID/{task_id}")
def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo_id(db, task_id)

@app.delete("/deleteTitle/{title}")
def delete_task_by_title(title: str, db: Session = Depends(get_db)):
    return crud.delete_todo_title(db, title)

@app.delete("/deleteAll")
def delete_all_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_todos(db)
