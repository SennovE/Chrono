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
    name = Column(String)
    text = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    recurring = Column(Boolean)
    week_day = Column(Integer)
    
    owner_id = Column(UUID, ForeignKey("Users.id"), index=True)
    author = relationship("User")