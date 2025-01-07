from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import DeclarativeBase
import uuid


class DeadlineTask(DeclarativeBase):
    __tablename__ = "Deadline_tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    author_id = Column(UUID, ForeignKey("Users.id"))

    author = relationship("User")

    deadline_time = Column(DateTime)
    description = Column(String)
    status = Column(Integer)     #0 - активно, 1 - завершено, 2 - просрочено
