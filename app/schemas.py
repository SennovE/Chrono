from pydantic import BaseModel, Field
from uuid import UUID


class UserResponse(BaseModel):
    id: int
    email: str = Field(unique=True)
    hashed_password: str

    class Config:
        from_attributes = True


class UserCreateForm(BaseModel):
    email: str = Field(unique=True)
    password: str = Field()


class TaskBase(BaseModel):
    id: int = Field(primary_key=True, index=True)
    author_id: int
