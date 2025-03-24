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
    author_id = Column(UUID)

    author = Column(String)

    deadline_time = Column(DateTime(timezone=True), nullable=True)
    
    description = Column(String)
    status = Column(Integer)     #0 - активно, 1 - завершено
