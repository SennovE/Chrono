import re
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

class TaskGroupBase(BaseModel):
    name: str
    color: str

    @field_validator("color")
    def validate_hex_color(cls, value):
        pattern = r'^#[0-9A-Fa-f]{6}$'
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid color format. Expected string like '00ff00'")
        return value


class TaskGroupForm(TaskGroupBase):
    id: UUID
    code: UUID


class UpdateTaskGroupForm(TaskGroupBase):
    id: UUID
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
