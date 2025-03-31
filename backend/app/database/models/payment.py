from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import DeclarativeBase
import uuid




class Payment(DeclarativeBase):
    __tablename__ = "Payments"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    id_user = Column(String, primary_key=True)
    email = Column(String)

