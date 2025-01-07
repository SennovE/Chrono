from pydantic import BaseModel, Field
from uuid import UUID


class DeadlineTaskDebugResponse(BaseModel):
    id: UUID
    author: str
    author_id: UUID
    deadline_time: str
    description: str
    status: int


class DeadlineTaskCreateForm(BaseModel):
    deadline_time: str = Field()
    description: str = Field()