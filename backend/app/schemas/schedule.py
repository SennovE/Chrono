from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ScheduleForm(BaseModel):
    text: str = Field(example="Meeting or task that you need to put to your schedule")
    start_time: datetime
    end_time: datetime
    recurring: bool = Field(description="Should your task be repeated every week?")


class ScheduleResponse(ScheduleForm):
    id: UUID
    week_day: int


class ScheduleUpdateForm(BaseModel):
    text: str | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    recurring: bool | None = Field(default=None)
