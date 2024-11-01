from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import DeclarativeBase


class DDTask(DeclarativeBase):
    __tablename__ = "DD_tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True
    )
    author_id = Column(UUID, ForeignKey("Users.id"))

    author = relationship("User")

    dd_time = Column(DateTime)
    description = Column(String)
