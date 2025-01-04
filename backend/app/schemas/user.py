from pydantic import BaseModel, Field
from uuid import UUID


class UserResponse(BaseModel):
    email: str = Field(unique=True)
    username: str | None
    premium: bool

    class Config:
        from_attributes = True


class UserDebugResponse(BaseModel):
    id: UUID
    email: str = Field(unique=True)
    hashed_password: str
    username: str | None
    premium: bool

    class Config:
        from_attributes = True


class UserCreateForm(BaseModel):
    email: str = Field(unique=True)
    password: str = Field()