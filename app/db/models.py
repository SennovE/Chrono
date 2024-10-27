from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db import DeclarativeBase
import uuid


class User(DeclarativeBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Column(default_factory=uuid.uuid4, primary_key=True)
    username = Column(String, index=True, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    premium = Column(Boolean, default=False)
    hashed_password = Column(String)


class Task(DeclarativeBase, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Column(default_factory=uuid.uuid4, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
