from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from datetime import datetime, timedelta
from uuid import UUID
class EmailUpdateForm(BaseModel):
    email: str = Field(unique=True)
class PasswordUpdateForm(BaseModel):
    password: str