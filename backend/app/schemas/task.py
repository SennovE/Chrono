from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime

class TaskForm(BaseModel):
    description: str = Field(examples=["What needs to be done?"])
    deadline_time: datetime = Field(description="Time when the task is due")
    author_id: UUID = Field(description="Unique identifier of the user associated with the task")
class TaskInfo(BaseModel):
    description: str = Field(examples=["What needs to be done?"])
    deadline_time: datetime = Field(description="Time when the task is due")
    
