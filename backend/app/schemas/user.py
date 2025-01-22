from pydantic import BaseModel, Field
from uuid import UUID


class UserResponse(BaseModel):
    email: str = Field(unique=True)
    username: str
    premium: bool


class UserDebugResponse(BaseModel):
    id: UUID
    email: str = Field(unique=True)
    username: str
    premium: bool
    password: str
    text_settings: str


class UserCreateForm(BaseModel):
    email: str = Field(unique=True)
    password: str = Field()


class UserTextSettings(BaseModel):
    text: str = Field()