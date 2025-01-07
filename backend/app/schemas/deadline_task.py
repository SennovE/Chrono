from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class DeadlineTaskDebugResponse(BaseModel):
    id: UUID
    author: str
    author_id: UUID
    deadline_time: datetime
    description: str
    status: int


class DeadlineTaskCreateForm(BaseModel):
    deadline_time: datetime = Field()
    description: str = Field()


class DeadlineTaskResponse(BaseModel):
    deadline_time: datetime = Field(default=datetime.today())
    description: str = Field(default="Описание дедлайна")
    status: int = Field(default=0)