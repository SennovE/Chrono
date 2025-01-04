from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import DeclarativeBase
import uuid


class User(DeclarativeBase):
    __tablename__ = "Users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True)
    premium = Column(Boolean, default=False)
    password = Column(String)
