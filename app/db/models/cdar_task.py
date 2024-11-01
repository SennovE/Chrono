from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import DeclarativeBase


class CdarTask(DeclarativeBase):
    __tablename__ = "Cdar_tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True
    )
    author_id = Column(UUID, ForeignKey("Users.id"))

    author = relationship("User")