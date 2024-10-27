from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base, table=True):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    premium = Column(Boolean, default=False)
    hashed_password = Column(String)


class Task(Base, table=True):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
