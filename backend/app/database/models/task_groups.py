from sqlalchemy import Column, ForeignKey, UUID, String
from sqlalchemy.orm import relationship

from app.database import DeclarativeBase
import uuid


class TaskGroup(DeclarativeBase):
    __tablename__ = "TaskGroup"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    code = Column(
        UUID(as_uuid=True), 
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )


class UserToGroup(DeclarativeBase):
    __tablename__ = "UserToGroup"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    user_id = Column(UUID, ForeignKey("Users.id"), index=True, nullable=False)
    user = relationship("User")
    group_id = Column(UUID, ForeignKey("TaskGroup.id"), nullable=False)
    group = relationship("TaskGroup")
