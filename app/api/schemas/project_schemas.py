from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import date

ProjectNameStr = constr(strip_whitespace=True, min_length=3, max_length=100)

class ProjectCreateSchema(BaseModel):
    name: ProjectNameStr # type: ignore
    user_id: int
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date:   Optional[date] = None
    status: Literal["active", "completed", "archived"] = "active"

class ProjectUpdateSchema(BaseModel):
    # all fields optional for partial update
    name: Optional[ProjectNameStr] = None # type: ignore
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date:   Optional[date] = None
    status: Optional[Literal["active", "completed", "archived"]] = None
