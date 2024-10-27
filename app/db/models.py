from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    username = Column(String, index=True, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    premium = Column(Boolean, default=False)
    hashed_password = Column(String)


class Task(DeclarativeBase):
    __tablename__ = "posts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True
    )
    author_id = Column(UUID, ForeignKey("users.id"))

    author = relationship("User")
