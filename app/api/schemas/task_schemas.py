from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import date, datetime

TitleStr = constr(strip_whitespace=True, min_length=3, max_length=100)

class TaskCreateSchema(BaseModel):
    title: TitleStr # type: ignore
    project_id: int
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Literal["low", "medium", "high"] = "medium"
    status:   Literal["pending", "in_progress", "completed"] = "pending"
    completed_at: Optional[datetime] = None

class TaskUpdateSchema(BaseModel):
    title: Optional[TitleStr] = None # type: ignore
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status:   Optional[Literal["pending", "in_progress", "completed"]] = None
    completed_at: Optional[datetime] = None
