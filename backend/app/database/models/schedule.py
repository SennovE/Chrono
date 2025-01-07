from sqlalchemy import Column, ForeignKey, UUID, DateTime, String, Boolean, Integer
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
    author_id = Column(UUID, ForeignKey("Users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    text = Column(String)
    recurring = Column(Boolean)
    week_day = Column(Integer)


    author = relationship("User")