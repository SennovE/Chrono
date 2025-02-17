from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from datetime import datetime, timedelta
from uuid import UUID


class ScheduleForm(BaseModel):
    name: str = Field(example="Name for your event")
    text: str | None = Field(example="Meeting or task that you need to put to your schedule")
    start_time: datetime = Field(example=datetime.today())
    end_time: datetime = Field(example=datetime.today() + timedelta(hours=1))
    recurring: bool = Field(default=False, description="Should your task be repeated every week?")

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_time >= self.end_time:
            raise PydanticCustomError(
                "time_error",
                "start_time should be less than end_time",
                {
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                }
            )
        return self


class ScheduleResponse(BaseModel):
    id: UUID
    name: str
    text: str | None
    year: int
    month: int
    day: int
    start_hours: int
    start_minutes: int
    end_hours: int
    end_minutes: int
    recurring: bool


class ScheduleUpdateForm(BaseModel):
    name: str | None = Field(default=None)
    text: str | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    recurring: bool | None = Field(default=None)


class ScheduleGenerate(BaseModel):
    text: str
    ''' TODO: настройки запроса, которые пользователь вводит для конкретной генерации на странице расписания, не из настроек'''


class ScheduleList(BaseModel):
  tasks: list[ScheduleUpdateForm]

  class Config:
        arbitrary_types_allowed = True