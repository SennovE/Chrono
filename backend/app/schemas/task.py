from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime


class TaskForm(BaseModel):
    task_description: str = Field(..., examples=["What needs to be done?"])
    time: datetime = Field(..., description="Time when the task is due")
    user_id: UUID = Field(..., description="Unique identifier of the user associated with the task")

