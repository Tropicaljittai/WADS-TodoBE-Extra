from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    todo_id = Column(Integer, primary_key=True, index= True)
    title = Column(String[50])
    completed = Column(Boolean)
    

