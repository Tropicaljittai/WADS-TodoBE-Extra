from typing import Union
from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, description="New todo title")
    completed: Optional[bool] = Field(None, description="Check if todo is done yet or not")