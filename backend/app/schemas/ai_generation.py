from pydantic import BaseModel


class DeadlineGenerate(BaseModel):
    text: str