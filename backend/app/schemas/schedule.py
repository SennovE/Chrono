from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from datetime import datetime, timedelta
from uuid import UUID


class ScheduleForm(BaseModel):
    text: str = Field(example="Meeting or task that you need to put to your schedule")
    start_time: datetime = Field(default=datetime.today())
    end_time: datetime = Field(default=datetime.today() + timedelta(hours=1))
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


class ScheduleResponse(ScheduleForm):
    id: UUID
    week_day: int = Field(default=datetime.today().weekday())


class ScheduleUpdateForm(BaseModel):
    text: str | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    recurring: bool | None = Field(default=None)


class ScheduleDebugForm(BaseModel):
    id: UUID
    text: str | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    recurring: bool | None = Field(default=None)
    week_day: int | None = Field(default=None)
    owner_id: UUID = Field(default=None)
