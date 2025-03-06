from pydantic import BaseModel
from uuid import UUID


class TaskGroupBase(BaseModel):
    name: str
    color: str


class TaskGroupForm(TaskGroupBase):
    id: UUID
