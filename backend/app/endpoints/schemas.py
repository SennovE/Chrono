from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    id: int = Field(primary_key=True, index=True)
    author_id: int