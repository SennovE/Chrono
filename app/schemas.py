from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    name: str
    email: str = Field(unique=True)
    premium: bool = Field(default=False)
    hashed_password: str


class UserCreateForm(BaseModel):
    email: str = Field(unique=True)
    password: str = Field()


class TaskBase(BaseModel):
    id: int = Field(primary_key=True, index=True)
    author_id: int
    author = User
