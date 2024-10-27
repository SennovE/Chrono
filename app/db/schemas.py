from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(index=True, unique=True)
    name: str
    email: str = Field(unique=True)
    premium: bool = Field(default=False)
    hashed_password: str


class User(UserBase):
    id: int = Field(primary_key=True, index=True)

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    author_id: int


class Task(UserBase):
    id: int = Field(primary_key=True, index=True)
    author = User

    class Config:
        orm_mode = True