from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import DeclarativeBase
import uuid


class CdarTask(DeclarativeBase):
    __tablename__ = "Cdar_tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    author_id = Column(UUID, ForeignKey("Users.id"))

    author = relationship("User")