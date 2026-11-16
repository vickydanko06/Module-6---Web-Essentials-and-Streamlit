# project/starter/app/schemas/task.py
# Module 5 Project — Task schemas
#
# TODO: Define TaskCreate, TaskPatch, TaskResponse

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class TaskCreate(BaseModel):
    """Input for creating a task."""
    # TODO: title, description (optional), completed (default False)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)


class TaskPatch(BaseModel):
    """Input for partial task update."""
     # TODO: all Optional fields
    title: Optional[str] = None
    description: Optional[str]= None
    completed: Optional[bool] = Field(default=None)


class TaskResponse(TaskCreate):
    """Returned to clients."""
    # TODO: id, owner_id + model_config
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
