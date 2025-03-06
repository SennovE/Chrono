from sqlalchemy import Column, ForeignKey, UUID, String, Boolean, Integer
from sqlalchemy.orm import relationship

from app.database import DeclarativeBase
import uuid


class Schedule(DeclarativeBase):
    __tablename__ = "Schedule"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    name = Column(String)
    text = Column(String, nullable=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    start_hours = Column(Integer)
    start_minutes = Column(Integer)
    end_hours = Column(Integer)
    end_minutes = Column(Integer)
    recurring = Column(Boolean)
    week_day = Column(Integer)
    
    owner_id = Column(UUID, ForeignKey("Users.id"), index=True)
    author = relationship("User")
    group_id = Column(UUID, ForeignKey("TaskGroup.id"), index=True, nullable=True)
    task_group = relationship("TaskGroup")


class TaskGroup(DeclarativeBase):
    __tablename__ = "TaskGroup"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    name = Column(String)
    color = Column(String)
    owner_id = Column(UUID, ForeignKey("Users.id"), index=True)
    author = relationship("User")
