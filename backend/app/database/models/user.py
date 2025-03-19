from sqlalchemy import Column, DateTime, String, Boolean, UUID, func

from app.database import DeclarativeBase
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
class BlackList(DeclarativeBase):
    __tablename__ = "BlackList"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())